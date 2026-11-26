"""Search scope (REQ-24, DD-5) on the F-REPO repository, with extra files planted in the base commit.

The scope is tracked files under tests/, scripts/, docs/, root-level files, change-log style files anywhere, the
directories of plan-named paths and same-basename mirrors of plan-named files; `.dev/` and dependency folders
are out, wherever they sit. Git runs only inside the repository built under /tmp.
"""

import json

from fixtures.repos.build_repo import EDITED, MIRROR, TRAP_MARKER, build_repo
from sweep import extractors, plan
from sweep.extractors import Ctx

TOKEN = "report_exporter"
PLAN_TEXT = (
    f"## Task 1: Edit the exporter\n\nEdit `{EDITED}` to write 3 report formats.\n"
)
EXTRA = {
    # in scope
    "tests/test_scope_hit.py": f"# {TOKEN}\n",
    "docs/doc_hit.md": f"{TOKEN}\n",
    "pkg/sub/CHANGES.txt": f"- {TOKEN}\n",
    "src/exporter/notes.py": f"# {TOKEN}\n",  # a directory the plan names
    MIRROR: f"# {TOKEN}\n",  # same basename as the plan-named report.py
    # out of scope
    "pkg/sub/other.txt": f"{TOKEN}\n",
    "other/dir/x.py": f"# {TOKEN}\n",
    "tests/node_modules/dep.js": f"// {TOKEN}\n",
    "docs/vendor/y.md": f"{TOKEN}\n",
    "tests/.dev/n.md": f"{TOKEN}\n",
    "tests/ground-truth.json": f'{{"x": "{TRAP_MARKER}"}}\n',
}
INCLUDED = {
    "README.md",  # a root document
    "scripts/export.sh",
    "tests/test_scope_hit.py",
    "docs/doc_hit.md",
    "pkg/sub/CHANGES.txt",
    "src/exporter/notes.py",
    MIRROR,
}
EXCLUDED = {
    ".dev/notes/search-noise.md",
    "node_modules/pkg/index.js",
    "pkg/sub/other.txt",
    "other/dir/x.py",
    "tests/node_modules/dep.js",
    "docs/vendor/y.md",
    "tests/.dev/n.md",
}


def make(root, text=PLAN_TEXT):
    built = build_repo(root, extra=EXTRA)
    return built, Ctx(plan.parse(text), snapshot=built.repo, seed=1)


def hit_paths(ctx, *patterns):
    return {h.path for h in extractors.search(ctx, list(patterns))}


def holding(ctx, paths, token):
    """The paths whose text holds token (a ground-truth fixture is never opened here)."""
    return {
        p
        for p in paths
        if not p.rpartition("/")[2].startswith("ground-truth")
        and token in (ctx.snapshot / p).read_text(errors="ignore")
    }


def test_dev_and_dependency_folders_excluded(tmp_roots):
    _, ctx = make(tmp_roots.root)
    paths = hit_paths(ctx, TOKEN)
    # the noise is really in the tree, so the exclusion is what keeps it out
    assert EXCLUDED <= holding(ctx, ctx.scope.tracked, TOKEN)
    assert not paths & EXCLUDED
    assert not [p for p in paths if p.startswith(".dev/") or "/.dev/" in p]
    assert not [p for p in paths if "node_modules/" in p or "/vendor/" in p]
    # the same holds for what the scope reports as its files
    assert not set(ctx.scope.files) & EXCLUDED
    # a ground-truth file is never searched (REQ-34), even in an in-scope folder
    assert hit_paths(ctx, TRAP_MARKER) == set()
    assert (
        "tests/ground-truth.json" not in ctx.scope.files
        and "ground-truth.json" not in ctx.scope.files
    )


def test_named_paths_and_mirrors_included(tmp_roots):
    _, ctx = make(tmp_roots.root)
    assert EDITED in ctx.named_paths
    paths = hit_paths(ctx, TOKEN)
    assert INCLUDED <= paths, INCLUDED - paths
    assert "src/exporter" in ctx.scope.named_dirs and "report.py" in ctx.scope.mirrors
    # what the helper searches is exactly the files the scope lists (pathspecs and file list agree)
    # (the pre-existing .dev noise is repeated in the tracked files, so compare through the same token)
    assert paths == holding(ctx, ctx.scope.files, TOKEN)


def test_scope_follows_the_plan(tmp_roots):
    # a plan that names another folder and another file brings those in, and drops the first plan's folder
    _, ctx = make(tmp_roots.root, text="## Task 1: x\n\nEdit `other/dir/x.py` now.\n")
    paths = hit_paths(ctx, TOKEN)
    assert "other/dir/x.py" in paths and "src/exporter/notes.py" not in paths
    assert MIRROR not in paths


def test_scope_string_recorded(tmp_roots):
    _, ctx = make(tmp_roots.root)
    s = ctx.scope_string
    assert isinstance(s, str) and s == ctx.scope.string
    assert (
        "tests/, scripts/, docs/" in s and "root-level files" in s and "change-log" in s
    )
    assert ".dev/" in s and "node_modules" in s
    assert (
        "src/exporter" in s and "report.py" in s
    )  # the plan-named folder and mirror name
    assert f"files in scope: {len(ctx.scope.files)}" in s
    assert "/tmp" not in s and str(ctx.snapshot) not in s  # repo-relative names only
    assert json.loads(json.dumps({"scope": s}))["scope"] == s
    # same input, same string; another plan, another string
    _, again = make(tmp_roots.root.parent / (tmp_roots.root.name + "-again"))
    assert again.scope_string == s
    other = Ctx(
        plan.parse("## Task 1: x\n\nEdit `other/dir/x.py`.\n"), snapshot=ctx.snapshot
    )
    assert other.scope_string != s and "other/dir" in other.scope_string
