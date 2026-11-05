# Tier 1 observation
- Source read (orchestrator): refs/conflict-mechanical.md:82-94. Tier 1 step 5 seeds uv.lock from the PR side and runs `uv lock` then `uv lock --check` on the merged work tree. Nothing reads the merged pyproject.toml before `uv lock`.
- Source read: conflicts.py:203-209: the only mechanical rule is uv.lock, derived from pyproject.toml; Tier 1 is reached by `regen_only` plans (conflicts.py:791-792), so pyproject.toml itself auto-merged (it is not a conflicted path in a Tier 1 plan).
- Codex reported a reproduction (only uv.lock conflicted, backend-path = ["."]).

## Probe (run 2026-11-04T22:14:40Z, same-shell, scratch project under /tmp, throwaway UV_CACHE_DIR, --offline; command: bash probe-lock-trust.sh; full output in probe-lock-trust.out)
    == uv lock --offline on a project with backend-path=["."] and dynamic version
    exit=1
          hint: This usually indicates a problem with the package or the build
          environment.
    in-tree backend executed: yes

## Behaviour definitions
- (a) observed: `uv lock` imported the in-tree module named by `build-backend` through `backend-path = ["."]` because `[project].dynamic` required metadata from the backend; the module's import side effect ran (marker file written) even though `uv lock` then failed (probe-lock-trust.out:2-6).
- (b) not observed here, asserted by uv's resolver design: a `[tool.uv.sources]` path or editable source makes uv build that local package's metadata the same way. Covered by the owner's trigger list, not by this probe.
