# T6 evidence: astral-sh/setup-uv

## Doc sources consulted (2026-10-22)

- Context7 `/astral-sh/setup-uv` README: `python-version` sets the `UV_PYTHON` environment variable. `activate-environment` ("Use uv venv to activate a venv ready to be used by later steps") defaults to `"false"`. `VIRTUAL_ENV` is set only when `activate-environment` is true.
- `action.yml` at tag v10.3.2 (`gh api 'repos/astral-sh/setup-uv/contents/action.yml?ref=v10.3.2'`):
  - line 12 `python-version:` "The version of Python to set UV_PYTHON to."
  - line 18 `activate-environment:` default `"false"`
  - line 21 `venv-path:` defaults to `.venv` in the working directory

## Tag chosen: `astral-sh/setup-uv@v10.3.2` (full release tag, not `@v10`)

Latest release: `gh api repos/astral-sh/setup-uv/releases/latest --jq .tag_name` printed `v10.3.2`.

Tag-existence checks:

```
$ gh api repos/astral-sh/setup-uv/git/ref/tags/v10 2>&1
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/git/refs#get-a-reference","status":"404"}gh: Not Found (HTTP 404)
(exit 1)

$ gh api repos/astral-sh/setup-uv/git/ref/tags/v10.3.2 2>&1
{"ref":"refs/tags/v10.3.2","node_id":"REF_kwDOMnghHrFyZWZzL3RhZ3MvdjEwLjMuMg","url":"https://api.github.com/repos/astral-sh/setup-uv/git/refs/tags/v10.3.2","object":{"sha":"07a047e608db84b3d8c06cd9a7c7dcc9c355c18e","type":"commit","url":"https://api.github.com/repos/astral-sh/setup-uv/git/commits/07a047e608db84b3d8c06cd9a7c7dcc9c355c18e"}}(exit 0)
```

setup-uv does not publish a floating major tag `v10`. As Task 6 directs, the full release tag `v10.3.2` is used instead. This differs from the repo's other actions (`@v4`, `@v5`). Future setup-uv upgrades need a manual tag bump, or Dependabot.

## verify-deps: the planned "widening" was a regression, so the old audit scope is kept (necessary deviation)

The plan expected the widened audit to pass. A local reproduction in the worktree on 2026-10-22 shows it fails:

```
$ uv venv --python 3.10 .venv && . .venv/bin/activate && python --version
Python 3.10.20
$ uv pip install -e ".[dev]"
(exit 0)
$ make verify-deps            # activated [dev] venv == uv's project env (.venv)
FAIL: new top-level dependencies detected outside AC3 allow-list:
  + py-cpuinfo2
make: *** [Makefile:358: verify-deps] Error 1
```

Cause:
- `uv pip install -e ".[dev]"` resolves fresh and ignores `uv.lock`. It pulls `py-cpuinfo2`, which is not in `scripts/dependency_baseline.txt`; the baseline lists `py-cpuinfo`.
- The old CI never hit this. With `--system` installs, `uv run` built its own project `.venv` from `uv.lock`, and that environment passes.
- With `activate-environment: true`, the activated `.venv` is also uv's project environment, so `uv run` audits the fresh `[dev]` install instead.

Today's CI setup, a separate project env, passes:

```
$ UV_PROJECT_ENVIRONMENT=/tmp/t6-oldci-venv make verify-deps
PASS: installed packages are a subset of the AC3 allow-list.
EXIT=0
```

Fix: give the `Verify dependency allow-list` step `env: UV_PROJECT_ENVIRONMENT: ${{ runner.temp }}/verify-deps-venv`. `uv run` then builds a separate `uv.lock`-resolved env, exactly as before. Checked locally with the `[dev]` venv activated, as it is in CI:

```
$ . .venv/bin/activate   # VIRTUAL_ENV=.venv
$ UV_PROJECT_ENVIRONMENT=/tmp/t6-sep-venv make verify-deps
warning: `VIRTUAL_ENV=.venv` does not match the project environment path `/tmp/t6-sep-venv` and will be ignored
PASS: installed packages are a subset of the AC3 allow-list.
EXIT=0
```

Other steps are unaffected. `pytest`, `ruff` and `superclaude` resolve from the activated venv (`which` -> `.venv/bin/...`). Task 7, which merges this job into `lint`, must carry the same `env:` on its `make verify-deps` step.

Separate, pre-existing issue, not fixed here (out of scope): `uv pip install -e ".[dev]"` already resolves `py-cpuinfo2`, so any local `[dev]` install outside `uv.lock` would fail verify-deps. The baseline file is outside this plan's scope.

## doctor-check

The steps `origin/master` added (`permissions: contents: read`, checkout `persist-credentials: false`, `Set up Node`, `Install Claude CLI`) are kept unchanged. The setup-uv step takes the place of `Set up Python`, before `Set up Node`.
