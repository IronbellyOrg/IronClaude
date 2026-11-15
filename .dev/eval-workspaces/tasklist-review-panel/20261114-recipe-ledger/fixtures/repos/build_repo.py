"""F-REPO (TESTING section 2): build a small invented git repository under /tmp and return its base and head commits.

The repository holds every shape the sandbox, the extractors' repository search and the scope tests need:
tests/, scripts/, docs/, root files, CHANGELOG.md, a mirror copy of a plan-named file, `.dev/` and
`node_modules/` noise that repeats every search string, files the sandbox builder must remove (H4), a
trap file named ground-truth.json that holds invented text only, and one "implementation" commit that
adds a file and edits another. Git runs inside the new repository only.
"""

import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

DOC_ID = "TASK-WF-fixture-20261114-000001"
OTHER_DOC_ID = "TASK-WF-fixture-20261114-000002"
TRAP_MARKER = "TRAP-INVENTED-TEXT-7f3a"
# strings that a plan sentence would make the search helper look for; the noise files repeat all of them
SEARCH_STRINGS = (
    "report_exporter",
    "retention_policy",
    "3 report formats",
    "report.py",
)

ADDED = "src/exporter/retention.py"
EDITED = "src/exporter/report.py"
MIRROR = "plugins/exporter-mirror/src/exporter/report.py"

REPORT_BASE = '''"""Render a report in one of three formats."""

FORMATS = ("csv", "json", "html")


def render(rows, fmt="csv"):
    if fmt not in FORMATS:
        raise ValueError(fmt)
    return "\\n".join(",".join(str(c) for c in r) for r in rows)
'''
REPORT_HEAD = REPORT_BASE.replace(
    "    return", "    # retention is applied by the caller\n    return"
)
RETENTION = '''"""Retention policy: keep a report for 30 days."""

KEEP_DAYS = 30


def expired(age_days):
    return age_days > KEEP_DAYS
'''


def _noise():
    s = "\n".join(f"- {x}" for x in SEARCH_STRINGS)
    return f"Invented search noise. Every search string appears here:\n{s}\n"


def _files(doc_id):
    noise = _noise()
    return {
        # root files and documents
        "README.md": f"# Fixture exporter\n\n{noise}",
        "Makefile": "test:\n\tpytest\n",
        ".gitignore": "node_modules/\n*.log\n",
        "CHANGELOG.md": "# Changelog\n\n- 0.1.0: first release (3 report formats)\n",
        "docs/guide.md": (
            "# Exporter guide\n\n## Retention policy\n\n"
            "The exporter writes 3 report formats: csv, json and html.\n"
        ),
        "docs/progress.md": "invented progress note outside any task folder\n",
        # code, tests, scripts, the mirror copy
        EDITED: REPORT_BASE,
        MIRROR: REPORT_BASE,
        "src/exporter/__init__.py": "",
        "tests/test_report.py": (
            "from exporter.report import render\n\n\n"
            "def test_render():\n    assert render([[1, 2]]) == '1,2'\n"
        ),
        "scripts/export.sh": "#!/usr/bin/env bash\necho report_exporter\n",
        # noise that must not reach any evidence
        ".dev/notes/search-noise.md": noise,
        "node_modules/pkg/index.js": f"// {noise}",
        # files the sandbox builder removes (H4)
        ".dev/reflect/REFLECT-REPORT.md": "invented reflect report\n",
        f".dev/tasks/done/{doc_id}/source.md": f"# Source of {doc_id}\n\n{noise}",
        f".dev/tasks/done/{doc_id}/progress.md": "invented ledger\n",
        f".dev/tasks/done/{OTHER_DOC_ID}/notes.md": "invented notes\n",
        ".dev/tasks/to-do/other/artifacts/out.txt": "invented artifact\n",
        ".dev/tasks/to-do/other/progress.md": "invented ledger\n",
        ".dev/eval-workspaces/ws/candidate.md": "invented candidate\n",
        ".dev/research/r1.md": "invented research note\n",
        f".dev/misc/{doc_id}-notes.md": "invented note with the document id in its path\n",
        "artifacts/build.log": "invented build output\n",
        # traps: invented text only
        "ground-truth.json": f'{{"note": "{TRAP_MARKER}"}}\n',
        ".dev/gt/ground-truth.json": f'{{"note": "{TRAP_MARKER}"}}\n',
    }


def _git(repo, *args):
    """Run git in repo only, with no user, system or hook configuration."""
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith(("GIT_", "SW_", "FAKE_"))
    }
    env.update(
        GIT_CONFIG_GLOBAL="/dev/null",
        GIT_CONFIG_NOSYSTEM="1",
        GIT_AUTHOR_NAME="fixture",
        GIT_AUTHOR_EMAIL="fixture@localhost",
        GIT_COMMITTER_NAME="fixture",
        GIT_COMMITTER_EMAIL="fixture@localhost",
    )
    r = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return r.stdout.strip()


def _put(repo, rel, text):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def build_repo(root, doc_id=DOC_ID, extra=None):
    """Create root/repo (root must be under /tmp) and return a namespace of facts.

    extra: {path: text} committed in the base commit as well (a test plants a leak with it).
    Fields: repo, base, head, doc_id, added, edited, mirror, source_rel, trap_marker, search_strings.
    """
    repo = Path(root).resolve() / "repo"
    if not str(repo).startswith("/tmp/"):
        raise ValueError(f"build_repo writes only under /tmp: {repo}")
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    for rel, text in {**_files(doc_id), **(extra or {})}.items():
        _put(repo, rel, text)
    _git(repo, "add", "-A", "-f")
    _git(repo, "commit", "-q", "-m", "base")
    base = _git(repo, "rev-parse", "HEAD")
    # the implementation commit: one file added, one file edited
    _put(repo, ADDED, RETENTION)
    _put(repo, EDITED, REPORT_HEAD)
    _git(repo, "add", "-A", "-f")
    _git(repo, "commit", "-q", "-m", "implementation")
    head = _git(repo, "rev-parse", "HEAD")
    return SimpleNamespace(
        repo=repo,
        base=base,
        head=head,
        doc_id=doc_id,
        added=ADDED,
        edited=EDITED,
        mirror=MIRROR,
        source_rel=f".dev/tasks/done/{doc_id}/source.md",
        trap_marker=TRAP_MARKER,
        search_strings=SEARCH_STRINGS,
    )
