"""C4 probe: a pre-commit hook that rewrites and stages an unrelated tracked file.
Does finish-merge.sh publish a merge commit whose tree differs from the index it
validated? Uses the repository's own hermetic fixtures (scratch repos under /tmp)."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
import tests.pr_submit.test_conflict_scripts as t  # noqa: E402

with tempfile.TemporaryDirectory() as d:
    repos = t.make_repos(Path(d), {"README.md": "readme\n", "f.txt": "line1\nline2\nline3\n",
                                   "unrelated.txt": "original\n"})
    t._content_conflict(repos)
    setup = t.start_merge(repos)
    t.resolve(repos, {"f.txt": t.RESOLVED_F})
    hook = repos.work / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\nprintf 'changed by hook\\n' > unrelated.txt\ngit add unrelated.txt\n")
    hook.chmod(0o755)
    validated_tree = repos.git(repos.work, "write-tree").strip()
    res = t.finish_commit(repos, setup, ["f.txt"])
    print("finish stdout:", res.stdout.strip())
    print("exit:", res.returncode)
    committed_tree = repos.git(repos.work, "rev-parse", "HEAD^{tree}").strip()
    print("validated index tree:", validated_tree)
    print("committed tree:      ", committed_tree)
    print("unrelated.txt in HEAD:", repos.git(repos.work, "show", "HEAD:unrelated.txt").strip())
