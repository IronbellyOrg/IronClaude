"""Extractor core and the repository search helper (DESIGN section 4.1, DD-5, DD-10, section 5.1 step 2).

    Candidate           what an extractor finds (the fields of DESIGN 4.1; `cls` holds the JSON key `class`)
    Ctx                 parsed candidate, parsed source or None, snapshot root or None, seed, constants; the search
                        scope (DD-5) is built on first use and `Ctx.scope_string` is the text Task 22 records
    EXTRACTORS          {"E1": (find_e1, attach_e1), ...}; empty here, each extractor registers its pair
    run_extractors      the two phases of DD-10: `find` for every extractor, then `attach` only for the top K
                        candidates of each class (K_single when one class alone has candidates)
    search              one `git grep -F -f` per call over the DD-5 scope, in the snapshot only
    find_e2, attach_e2  extractor E2 (class C4, DESIGN 4.3): a literal pattern against the text the plan orders
    find_e3, attach_e3  extractor E3 (class C8, DESIGN 4.4): files that refer to a file the plan edits
    find_e4, attach_e4  extractor E4 (class C5, DESIGN 4.5): a count or "no remaining" claim and the places that carry it
    find_e1, attach_e1  extractor E1 (classes C1 and C6, DESIGN 4.2): set words and the scope they name
    find_e5, attach_e5  extractor E5 (class C2, DESIGN 4.6): source rules whose identifiers no citing task carries
    find_e7, attach_e7  extractor E7 (class C7, DESIGN 4.8): constraint clauses that dictated text leaves out
    find_e6, attach_e6  extractor E6 (class C3, experimental, DESIGN 4.7): a value that is read and never written

Candidate.status values set here: `found` (as made by `find`), `attached` (evidence computed, not yet decided) and
`dropped:pre_rank` (below the top K of its class; no evidence). select.py sets the rest: `selected`,
`dropped:quota`, `dropped:ceiling`, `dropped:cap12`, `no_evidence_slot`.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shlex
import subprocess
import tempfile
import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import NamedTuple

from scaffold import cards, fnd
from sweep import formats, plan, words

SW = Path(__file__).resolve().parents[1]
VALUES = SW / "config" / "values.json"

CLASSES = tuple(f"C{i}" for i in range(1, 9))
EXTRACTOR_IDS = tuple(f"E{i}" for i in range(1, 8))

STATUS_FOUND = "found"
STATUS_ATTACHED = "attached"
STATUS_PRE_RANK = "dropped:pre_rank"

ANCHOR_MIN, ANCHOR_MAX = 12, 200
EVIDENCE_MAX, EVIDENCE_TEXT_MAX = 5, 160

# the repository search helper (DESIGN 4.1)
MAX_HITS_PER_FILE = 3
MAX_LINES = 5000
HIT_TEXT_MAX = 500  # a stored hit line is cut here after the pattern test, so a minified file cannot fill memory

# the DD-5 scope
TOP_DIRS = ("tests", "scripts", "docs")
DEV_DIR = ".dev"
DEPENDENCY_DIRS = (
    "node_modules",
    "vendor",
    "bower_components",
    "jspm_packages",
    ".venv",
    "venv",
    "site-packages",
    ".tox",
    ".eggs",
    "__pycache__",
)
CHANGELOG_NAME = re.compile(
    r"^(change[-_]?logs?|changes|history|news|release[-_]?notes|releases)(\.[\w-]+)*$",
    re.IGNORECASE,
)
GROUND_TRUTH_NAME = re.compile(
    r"^ground[-_]truth", re.IGNORECASE
)  # REQ-34: never searched
_PATH_TOKEN = re.compile(formats.PATH_TOKEN)
_GREP_LINE = re.compile(r"^(.+?):(\d+):(.*)$", re.DOTALL)


class SearchError(RuntimeError):
    """The repository search cannot run (a pre-pass error, so the run falls back)."""


class NotAGitRepo(SearchError):
    """The snapshot root is not the top of a git repository."""


@dataclass
class Candidate:
    extractor: str
    cls: str
    kind: str
    anchor_text: str
    location: dict
    evidence: list = field(default_factory=list)
    features: dict = field(default_factory=dict)
    pre_priority: int = 0
    priority: int | None = None
    route: str = ""
    status: str = STATUS_FOUND
    evidence_computed: bool = False

    def to_dict(self) -> dict:
        """One entry of candidates.json (the key `class` is the DESIGN name of `cls`)."""
        return {
            "extractor": self.extractor,
            "class": self.cls,
            "kind": self.kind,
            "anchor_text": self.anchor_text,
            "location": dict(self.location),
            "evidence": [dict(e) for e in self.evidence],
            "features": dict(self.features),
            "pre_priority": self.pre_priority,
            "priority": self.priority,
            "route": self.route,
            "status": self.status,
            "evidence_computed": self.evidence_computed,
        }

    def validate(self, ctx: Ctx) -> None:
        """Raise ValueError when a field breaks a limit of DESIGN 4.1."""

        def bad(why):
            raise ValueError(
                f"{self.extractor} candidate {self.anchor_text[:40]!r}: {why}"
            )

        if self.extractor not in EXTRACTOR_IDS:
            bad(f"extractor {self.extractor!r}")
        if self.cls not in CLASSES:
            bad(f"class {self.cls!r}")
        if not ANCHOR_MIN <= len(self.anchor_text) <= ANCHOR_MAX:
            bad(f"anchor_text has {len(self.anchor_text)} characters")
        if fnd.flat(self.anchor_text) not in ctx.flat_text:
            bad("anchor_text is not an exact quote of the candidate")
        loc = self.location
        if not (
            isinstance(loc, dict)
            and "task" in loc
            and isinstance(loc.get("line_start"), int)
            and isinstance(loc.get("line_end"), int)
        ):
            bad("location needs task, line_start and line_end")
        for name in ("pre_priority", "priority"):
            v = getattr(self, name)
            if v is None and name == "priority":
                continue
            if not (isinstance(v, int) and 0 <= v <= 100):
                bad(f"{name} {v!r} is not an integer from 0 to 100")
        if len(self.evidence) > EVIDENCE_MAX:
            bad(f"{len(self.evidence)} evidence entries")
        for e in self.evidence:
            if not (
                isinstance(e, dict)
                and set(e) == {"path", "line", "text"}
                and isinstance(e["path"], str)
                and isinstance(e["line"], int)
                and isinstance(e["text"], str)
            ):
                bad(f"evidence entry {e!r} is not {{path, line, text}}")
            if e["path"].startswith("/") or ".." in e["path"].split("/"):
                bad(f"evidence path {e['path']!r} is not repo-relative")
            if len(e["text"]) > EVIDENCE_TEXT_MAX:
                bad(f"evidence text has {len(e['text'])} characters")


# The registry: id -> (find, attach). find(doc, ctx) -> list[Candidate]; attach(cands, ctx) -> None.
EXTRACTORS: dict[str, tuple[Callable, Callable]] = {}


def load_constants(path: Path | str = VALUES) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _clean_named(token: str) -> str | None:
    p = token
    while p.startswith("./"):
        p = p[2:]
    if not p or p.startswith("/") or "*" in p or any(c in p for c in "\n\r\0"):
        return None
    if any(seg in ("", "..") for seg in p.rstrip("/").split("/")):
        return None
    return p


def named_paths(doc: plan.Doc) -> tuple[str, ...]:
    """Every repo-relative path the plan names: its edit-target paths and every path-like token in its text.

    Absolute paths, paths with a `..` segment and glob patterns are left out, so a plan cannot point the search
    outside the snapshot.
    """
    found = {_clean_named(b["path"]) for b in doc.of("edit_target") if b.get("path")}
    found |= {_clean_named(m.group(0)) for m in _PATH_TOKEN.finditer(doc.text)}
    found.discard(None)
    return tuple(sorted(found))


@dataclass(frozen=True)
class Scope:
    """The DD-5 search scope of one snapshot: the tracked files it covers and the git pathspecs that select them."""

    tracked: tuple[str, ...]
    files: tuple[str, ...]
    pathspecs: tuple[str, ...]
    named_dirs: tuple[str, ...]
    mirrors: tuple[str, ...]
    string: str


def _git_env() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        LC_ALL="C",
        GIT_CONFIG_GLOBAL="/dev/null",
        GIT_CONFIG_NOSYSTEM="1",
        GIT_OPTIONAL_LOCKS="0",
    )
    return env


def git_root(snapshot) -> Path:
    """The resolved snapshot root; raises NotAGitRepo unless it is itself the top of a git repository.

    A plain folder inside some other repository is refused too, so a search can never reach that outer tree.
    """
    root = Path(snapshot).resolve()
    if not root.is_dir():
        raise NotAGitRepo(f"snapshot is not a directory: {root}")
    r = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True,
        env=_git_env(),
    )
    if r.returncode != 0:
        raise NotAGitRepo(f"snapshot is not a git repository: {root}")
    if Path(r.stdout.decode("utf-8", "replace").strip()).resolve() != root:
        raise NotAGitRepo(f"snapshot is not the top of its git repository: {root}")
    return root


def _tracked(root: Path) -> tuple[str, ...]:
    r = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"], capture_output=True, env=_git_env()
    )
    if r.returncode != 0:
        raise SearchError(
            f"git ls-files failed: {r.stderr.decode('utf-8', 'replace').strip()}"
        )
    return tuple(
        sorted(p for p in r.stdout.decode("utf-8", "replace").split("\0") if p)
    )


def _excluded(parts: list[str]) -> bool:
    return any(d == DEV_DIR or d in DEPENDENCY_DIRS for d in parts[:-1])


def build_scope(snapshot, named: tuple[str, ...] = ()) -> Scope:
    """DD-5: tracked files under tests/, scripts/, docs/; root-level files; change-log style files anywhere; the
    directories of plan-named paths; same-basename copies of plan-named files. `.dev/` and dependency folders out.
    """
    root = git_root(snapshot)
    tracked = _tracked(root)
    named_dirs = sorted(
        {
            d
            for p in named
            for d in [p.rstrip("/") if p.endswith("/") else p.rpartition("/")[0]]
            if d
        }
    )
    mirrors = sorted({p.rpartition("/")[2] for p in named if not p.endswith("/")})
    dirs = sorted(set(TOP_DIRS) | set(named_dirs))

    def in_scope(path: str) -> bool:
        parts = path.split("/")
        if _excluded(parts) or GROUND_TRUTH_NAME.match(parts[-1]):
            return False
        return (
            len(parts) == 1
            or any(path.startswith(d + "/") for d in dirs)
            or bool(CHANGELOG_NAME.match(parts[-1]))
            or parts[-1] in mirrors
        )

    files = tuple(f for f in tracked if in_scope(f))
    # directories as one pathspec each; the other files (root-level, change logs, mirrors) by name
    loose = [f for f in files if not any(f.startswith(d + "/") for d in dirs)]
    pathspecs = (
        [f":(literal){d}" for d in dirs]
        + [f":(literal){f}" for f in loose]
        + [f":(exclude,glob)**/{d}/**" for d in (DEV_DIR, *DEPENDENCY_DIRS)]
        + [":(exclude,glob,icase)**/ground[-_]truth*"]
    )
    string = "; ".join(
        [
            "tracked files under " + ", ".join(d + "/" for d in TOP_DIRS),
            "root-level files",
            "change-log style files anywhere (names: changelog, changes, history, news, release-notes, releases)",
            "directories of plan-named paths: " + (", ".join(named_dirs) or "none"),
            "same-basename mirrors of plan-named files: "
            + (", ".join(mirrors) or "none"),
            f"excluded: {DEV_DIR}/, dependency folders ({', '.join(DEPENDENCY_DIRS)}) and ground-truth files",
            f"files in scope: {len(files)}",
        ]
    )
    return Scope(
        tracked, files, tuple(pathspecs), tuple(named_dirs), tuple(mirrors), string
    )


@dataclass
class Ctx:
    """What every extractor gets: the parsed candidate, the parsed source or None, the snapshot root or None, the
    search scope (built on first use), the seed and the constants (config/values.json unless given)."""

    doc: plan.Doc
    source: plan.Doc | None = None
    snapshot: Path | None = None
    seed: int | str = 0
    constants: dict | None = None
    # ids of the tasks that cite no source section; `find_e5` sets it on every call (Task 22 writes it into
    # prepass.json as `tasks_without_citations`). It stays empty when there is no source, because E5 does not run.
    tasks_without_citations: list[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        if self.snapshot is not None:
            self.snapshot = Path(self.snapshot)
        if self.constants is None:
            self.constants = load_constants()

    @property
    def no_source(self) -> bool:
        """True when there is no source document: E5 returns nothing and the run records `no_source` (DESIGN 4.6)."""
        return self.source is None

    @property
    def not_applicable(self) -> dict[str, str]:
        """Classes that cannot be checked in this run, as {class: reason}; `{"C2": "no_source"}` without a source."""
        return {"C2": "no_source"} if self.no_source else {}

    @cached_property
    def named_paths(self) -> tuple[str, ...]:
        return named_paths(self.doc)

    @cached_property
    def scope(self) -> Scope:
        if self.snapshot is None:
            raise SearchError("no snapshot, so no search scope")
        return build_scope(self.snapshot, self.named_paths)

    @property
    def scope_string(self) -> str:
        """The scope as text, for prepass.json (REQ-24). It holds repo-relative names only."""
        return (
            "no snapshot: no repository search"
            if self.snapshot is None
            else self.scope.string
        )

    @cached_property
    def flat_text(self) -> str:
        return fnd.flat(self.doc.text)


class Hit(NamedTuple):
    path: str  # repo-relative
    line: int
    text: str  # the line, cut at HIT_TEXT_MAX
    pattern: str  # the first of the given patterns that the line contains


def search(ctx: Ctx, patterns, scope: Scope | None = None) -> list[Hit]:
    """One `git grep -n -I -F --no-color -f <patterns file> -- <pathspecs>` over the scope (default ctx.scope).

    LC_ALL=C; at most MAX_HITS_PER_FILE hits per file; only the first MAX_LINES output lines are read. Each
    hit's pattern is found here by plain substring tests, first pattern in the given order. Hits come in git's
    path order, then line order. Empty patterns and patterns with a line break are ignored. It raises SearchError
    when ctx has no snapshot and NotAGitRepo when the snapshot is not a git repository. Only tracked files of the
    snapshot are read (git does not follow a tracked symlink).
    """
    if ctx.snapshot is None:
        raise SearchError("no snapshot to search")
    root = git_root(ctx.snapshot)
    scope = scope if scope is not None else ctx.scope
    pats = list(
        dict.fromkeys(p for p in patterns if p and "\n" not in p and "\r" not in p)
    )
    if not pats:
        return []
    hits: list[Hit] = []
    per_file: dict[str, int] = {}
    with tempfile.TemporaryDirectory(prefix="sweep-grep-") as tmp:
        pfile, efile = Path(tmp) / "patterns.txt", Path(tmp) / "stderr.txt"
        pfile.write_text("\n".join(pats) + "\n", encoding="utf-8")
        argv = [
            "git", "-C", str(root), "grep", "-n", "-I", "-F", "--no-color",
            "-f", str(pfile), "--", *scope.pathspecs,
        ]  # fmt: skip
        truncated = False
        with efile.open("wb") as err:
            proc = subprocess.Popen(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=err,
                env=_git_env(),
            )
            try:
                for n, raw in enumerate(iter(proc.stdout.readline, b"")):
                    if n >= MAX_LINES:
                        truncated = True
                        proc.kill()
                        break
                    m = _GREP_LINE.match(raw.decode("utf-8", "replace").rstrip("\r\n"))
                    if not m or per_file.get(m[1], 0) >= MAX_HITS_PER_FILE:
                        continue
                    text = m[3]
                    pat = next((p for p in pats if p in text), None)
                    if pat is None:
                        continue
                    per_file[m[1]] = per_file.get(m[1], 0) + 1
                    hits.append(Hit(m[1], int(m[2]), text[:HIT_TEXT_MAX], pat))
            finally:
                proc.stdout.close()
                rc = proc.wait()
        if not truncated and rc not in (0, 1):
            msg = efile.read_text(encoding="utf-8", errors="replace").strip()
            raise SearchError(f"git grep failed (exit {rc}): {msg}")
    return hits


def _rank_key(seed, c: Candidate):
    """DESIGN 5.1 step 2: higher pre_priority first; ties by earlier plan line, then sha256(seed + anchor_text)."""
    digest = hashlib.sha256((str(seed) + c.anchor_text).encode("utf-8")).hexdigest()
    return (-c.pre_priority, c.location["line_start"], digest, c.extractor, c.kind)


def run_extractors(ctx: Ctx, registry: dict | None = None) -> list[Candidate]:
    """The two phases of DD-10; every candidate found is returned, in `find` order (extractor id order).

    1. `find` of every registered extractor (lexical, no repository access), then the candidates are grouped by
       class.
    2. The top K of each class by pre_priority get `attach` (K_single instead when only one class has any
       candidate), one `attach` call per extractor with its kept candidates. They get evidence_computed=True and
       status `attached`; `priority` falls back to pre_priority when attach leaves it unset.
    The rest keep no evidence, no final `priority` (None) and get status `dropped:pre_rank`. K and K_single come
    from ctx.constants.
    """
    registry = EXTRACTORS if registry is None else registry
    k, k_single = int(ctx.constants["K"]), int(ctx.constants["K_single"])
    routes = cards.routes()
    found: list[Candidate] = []
    for eid in sorted(registry):
        for c in registry[eid][0](ctx.doc, ctx):
            if c.extractor != eid:
                raise ValueError(f"{eid} produced a candidate of {c.extractor}")
            c.validate(ctx)
            c.route = c.route or routes[c.cls]
            c.status = STATUS_FOUND
            found.append(c)
    by_class: dict[str, list[Candidate]] = {}
    for c in found:
        by_class.setdefault(c.cls, []).append(c)
    keep = k_single if len(by_class) == 1 else k
    kept: set[int] = set()
    for group in by_class.values():
        group.sort(key=lambda c: _rank_key(ctx.seed, c))
        kept.update(id(c) for c in group[:keep])
        for c in group[keep:]:
            c.status = STATUS_PRE_RANK
    for eid in sorted(registry):
        batch = [c for c in found if c.extractor == eid and id(c) in kept]
        if not batch:
            continue
        registry[eid][1](batch, ctx)
        for c in batch:
            c.evidence_computed = True
            c.status = STATUS_ATTACHED
            if c.priority is None:
                c.priority = c.pre_priority
            c.priority = max(0, min(100, int(c.priority)))
            c.validate(ctx)
    return found


# ---------------------------------------------------------------- E2 (class C4): a literal pattern against ordered text
#
# DESIGN 4.3. `find_e2` is lexical (no repository access); `attach_e2` adds the evidence lines. The facts `attach_e2`
# needs travel in `Candidate.features`, so a candidate read back from candidates.json can still be attached.
# Evidence entries are {path, line, text}: `plan` entries carry the plan line of the ordered string; a fact about a
# file (the selector count, the base-checkout count) carries that file's repo-relative path and line 0 (no single line).

E2_FIRST_WORDS = ("grep", "egrep", "rg", "git", "pytest", "test")
_COMMAND_STARTS = ("grep ", "egrep ", "rg ", "git grep ", "pytest ")
E2_BASE_PRIORITY, E2_NO_MATCH, E2_NEAR_MISS, E2_SELECTOR_ZERO = 25, 45, 20, 5
PATTERN_MAX = 200  # a longer pattern is not converted (pattern_kind = regex_unparsed)
TEST_FILE_MAX = 1_000_000

_BACKTICKED = re.compile(r"`([^`\n]+)`")
_ORDERING = re.compile(
    r"(?<![\w-])(?:"
    + "|".join(
        re.escape(w) for w in sorted(words.ORDERING_VERBS, key=lambda w: (-len(w), w))
    )
    + r")(?![\w-])",
    re.IGNORECASE,
)
# the noun the sentence orders the string as, for the line "the task orders the heading ..."
_NOUNS = {
    "heading": "heading", "headings": "heading",
    "title": "title", "titles": "title", "titled": "title",
    "section": "section", "sections": "section",
    "label": "label", "labels": "label", "labelled": "label", "labeled": "label",
    "name": "name", "names": "name", "named": "name",
}  # fmt: skip
_NOUN = re.compile(r"(?<![\w-])(?:" + "|".join(_NOUNS) + r")(?![\w-])", re.IGNORECASE)
_SHELL_PUNCT = frozenset("|&;<>()")
_SAFE_PATH = re.compile(r"[\w.\-/+@%]+")
_COMPUTED = re.compile(
    r"\$[A-Za-z_{(]"
)  # a pattern built by the shell: not read (DESIGN 4.3 blind spot)
# options that take a value, per program (the value is not the pattern and not a path)
_SHORT_VALUE = {
    "grep": set("efmABCdD"),
    "egrep": set("efmABCdD"),
    "git grep": set("efABC"),
    "rg": set("efgmABCtTEjM"),
}
_LONG_VALUE = {
    "regexp", "file", "max-count", "include", "exclude", "exclude-dir", "after-context", "before-context",
    "context", "directories", "devices", "label", "binary-files", "max-depth", "threads", "glob", "type",
    "type-not", "max-columns", "encoding",
}  # fmt: skip
_PYTEST_SHORT_VALUE = set("kmpconWr")
_PYTEST_LONG_VALUE = {
    "maxfail", "rootdir", "junitxml", "tb", "deselect", "ignore", "ignore-glob", "confcutdir", "basetemp",
    "import-mode", "log-level", "capture", "color", "durations", "override-ini", "numprocesses", "dist", "timeout",
}  # fmt: skip
_POSIX_CLASS = {
    "alpha": "a-zA-Z", "digit": "0-9", "alnum": "a-zA-Z0-9", "upper": "A-Z", "lower": "a-z", "space": r"\s",
    "blank": r" \t", "punct": r"!-/:-@\[-`{-~", "xdigit": "0-9A-Fa-f", "word": r"\w",
}  # fmt: skip
_BRE_SPECIAL = frozenset(".[]*^$\\")
_ERE_SPECIAL = frozenset(".[]*^$\\+?(){}|")


def _shell_words(span: str) -> list[str] | None:
    """The words of a command line up to its first pipe, redirect or `;`; None when the quotes do not close."""
    lex = shlex.shlex(span, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    out: list[str] = []
    try:
        for tok in lex:
            if tok and set(tok) <= _SHELL_PUNCT:
                break
            out.append(tok)
    except ValueError:
        return None
    return out


def _clean_path(token: str) -> str | None:
    """A repo-relative path a command names, or None (absolute, `..`, glob, or anything the shell would expand)."""
    p = _clean_named(token)
    return p if p and _SAFE_PATH.fullmatch(p) and not p.startswith("-") else None


def _parse_grep(prog: str, args: list[str]) -> dict | None:
    """The pattern, flags and paths of a grep-family command; None when the pattern is not a plain word."""
    ext = prog in ("egrep", "rg")
    fixed = icase = word = False
    pattern: str | None = None
    computed = False
    positional: list[str] = []
    short_value = _SHORT_VALUE[prog]
    i, options_over = 0, False
    while i < len(args):
        a = args[i]
        i += 1
        if options_over or not a.startswith("-") or a == "-":
            positional.append(a)
        elif a == "--":
            options_over = True
        elif a.startswith("--"):
            name, eq, val = a[2:].partition("=")
            if name == "files":
                return None
            if name in ("ignore-case",):
                icase = True
            elif name == "fixed-strings":
                fixed = True
            elif name in ("extended-regexp", "perl-regexp"):
                ext = True
            elif name == "basic-regexp":
                ext = False
            elif name == "word-regexp":
                word = True
            elif name in _LONG_VALUE:
                if not eq:
                    val = args[i] if i < len(args) else ""
                    i += 1
                if name == "regexp" and pattern is None:
                    pattern = val
                elif name == "file":
                    computed = True
        else:
            cluster = a[1:]
            for j, ch in enumerate(cluster):
                if ch == "i":
                    icase = True
                elif ch == "F":
                    fixed = True
                elif ch in "EP" and ch not in short_value:
                    ext = True
                elif ch == "w":
                    word = True
                elif ch in short_value:
                    val = cluster[j + 1 :]
                    if not val:
                        val = args[i] if i < len(args) else ""
                        i += 1
                    if ch == "e" and pattern is None:
                        pattern = val
                    elif ch == "f":
                        computed = True
                    break
    if computed:
        return None
    if pattern is None:
        if not positional:
            return None
        pattern, positional = positional[0], positional[1:]
    if not pattern or "\n" in pattern or "\r" in pattern or _COMPUTED.search(pattern):
        return None
    paths = [p for p in (_clean_path(t) for t in positional) if p]
    return {
        "kind": "pattern", "pattern": pattern, "icase": icase, "fixed": fixed, "word": word, "ext": ext,
        "paths": list(dict.fromkeys(paths)),
    }  # fmt: skip


def _parse_pytest(args: list[str]) -> dict | None:
    """The selector of a pytest command (`-k`, `-m`, a `path::name` id); None when it names none."""
    k = m = None
    positional: list[str] = []
    i, options_over = 0, False
    while i < len(args):
        a = args[i]
        i += 1
        if options_over or not a.startswith("-") or a == "-":
            positional.append(a)
        elif a == "--":
            options_over = True
        elif a.startswith("--"):
            name, eq, _ = a[2:].partition("=")
            if name in _PYTEST_LONG_VALUE and not eq:
                i += 1
        else:
            cluster = a[1:]
            for j, ch in enumerate(cluster):
                if ch in _PYTEST_SHORT_VALUE:
                    val = cluster[j + 1 :]
                    if not val:
                        val = args[i] if i < len(args) else ""
                        i += 1
                    if ch == "k" and k is None:
                        k = val
                    elif ch == "m" and m is None:
                        m = val
                    break
    ids = [p.partition("::") for p in positional if "::" in p]
    files = [_clean_path(p.partition("::")[0]) for p in positional]
    files = [
        f for f in files if f and re.search(r"[^/.]\.\w+$", f)
    ]  # a file name, not a folder
    test_file = files[0] if files else None
    ident = next(
        (rest for f, _, rest in ids if rest and _clean_path(f) == test_file), None
    )
    if k is None and m is None and ident is None:
        return None
    return {
        "kind": "selector", "k": k, "m": m, "id": ident, "test_file": test_file,
        "paths": [test_file] if test_file else [],
    }  # fmt: skip


def _parse_command(span: str) -> dict | None:
    """A backticked span as a command of the DESIGN 4.3 families, or None when it is not one (or not readable)."""
    head = span.split(None, 1)[0] if span.strip() else ""
    if head not in E2_FIRST_WORDS:
        return None
    toks = _shell_words(span)
    if not toks:
        return None
    if toks[0] == "git" and toks[1:2] == ["grep"]:
        return _parse_grep("git grep", toks[2:])
    if toks[0] in ("grep", "egrep", "rg"):
        return _parse_grep(toks[0], toks[1:])
    if toks[0] == "pytest":
        return _parse_pytest(toks[1:])
    if (
        toks[0] == "test"
    ):  # `test "$(grep -c 'x' f)" -ge 1`: the grep inside is the pattern command
        inner = re.search(r"\$\(\s*((?:git grep|egrep|grep|rg)\b.*)\)", span)
        return _parse_command(inner.group(1)) if inner else None
    return None


def _to_python_regex(p: str, ext: bool) -> str | None:
    """A POSIX basic (`ext` False) or extended pattern as Python `re` syntax; None when it cannot be converted."""
    out: list[str] = []
    i, n = 0, len(p)
    while i < n:
        c = p[i]
        if c == "\\":
            if i + 1 >= n:
                return None
            d = p[i + 1]
            i += 2
            if not ext and d in "(){}|+?":
                out.append(d)
            elif d in "<>":
                out.append(r"\b")
            elif d.isalnum():
                out.append("\\" + d)
            else:
                out.append(re.escape(d))
        elif c == "[":
            j, body, neg = i + 1, [], ""
            if j < n and p[j] == "^":
                neg, j = "^", j + 1
            if j < n and p[j] == "]":
                body.append(r"\]")
                j += 1
            while j < n and p[j] != "]":
                if p.startswith("[:", j):
                    end = p.find(":]", j + 2)
                    name = p[j + 2 : end] if end != -1 else None
                    if name not in _POSIX_CLASS:
                        return None
                    body.append(_POSIX_CLASS[name])
                    j = end + 2
                    continue
                body.append("\\" + p[j] if p[j] in "\\[]^&~|" else p[j])
                j += 1
            if j >= n:
                return None  # no closing bracket
            out.append("[" + neg + "".join(body) + "]")
            i = j + 1
        elif not ext and c in "(){}|+?":
            out.append("\\" + c)
            i += 1
        elif not ext and c == "*" and (not out or out[-1] in ("(", "|", "^")):
            out.append(r"\*")  # a leading star of a basic pattern is a plain star
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _literal_test(cmd: dict, s: str) -> tuple[bool | None, str]:
    """(matched, pattern_kind): matched is None when the pattern cannot be read as a regular expression."""
    p, flags = cmd["pattern"], re.IGNORECASE if cmd["icase"] else 0
    special = _ERE_SPECIAL if cmd["ext"] else _BRE_SPECIAL
    if cmd["fixed"] or not any(ch in special for ch in p):
        if cmd["word"]:
            return bool(re.search(rf"(?<!\w){re.escape(p)}(?!\w)", s, flags)), "literal"
        return (p.lower() in s.lower() if cmd["icase"] else p in s), "literal"
    py = _to_python_regex(p, cmd["ext"]) if len(p) <= PATTERN_MAX else None
    if py is not None and cmd["word"]:
        py = rf"(?<!\w)(?:{py})(?!\w)"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rx = re.compile(py, flags) if py is not None else None
    except re.error:
        rx = None
    return (None, "regex_unparsed") if rx is None else (bool(rx.search(s)), "regex")


def _collapse(x: str) -> str:
    return re.sub(r"[-_\s]+", " ", x.lower()).strip()


def _words_of(x: str) -> set[str]:
    return {
        w
        for w in re.findall(r"[a-z0-9]+", re.sub(r"\\[a-zA-Z]", " ", x.lower()))
        if len(w) >= 3
    }


def _ordered_strings(doc: plan.Doc, order: dict[str, int]) -> list[dict]:
    """Double-quoted strings and backticked headings of sentences that hold an ordering verb, in plan order."""
    found: dict[tuple[str, int], dict] = {}
    for b in doc.of("task", "dictated_text"):
        text = b["text"]
        for start, _, sent in plan.sentences(text):
            if not _ORDERING.search(sent):
                continue
            ticks = [m.span() for m in _BACKTICKED.finditer(sent)]
            spans = [(m.start(1), m.group(1)) for m in _BACKTICKED.finditer(sent)]
            for pat in formats.QUOTED_SPANS:
                spans += [
                    (m.start("q"), m.group("q"))
                    for m in re.finditer(pat, sent)
                    if not any(
                        a <= m.start() < z for a, z in ticks
                    )  # a quote inside a command is not ordered
                ]
            for at, s in spans:
                s = s.strip()
                if len(s) < 2 or _parse_command(s) or s.startswith(_COMMAND_STARTS):
                    continue  # a command is not an ordered string
                if re.fullmatch(formats.PATH_TOKEN, s):
                    continue  # a path is not a heading
                line = b["line_start"] + text.count("\n", 0, start + at)
                nouns = _NOUN.findall(sent[:at])
                found.setdefault(
                    (s, line),
                    {
                        "text": s,
                        "line": line,
                        "at": start + at,
                        "noun": _NOUNS[nouns[-1].lower()] if nouns else "string",
                        "task": order.get(b["task"], -1),
                    },
                )
    return sorted(found.values(), key=lambda d: (d["line"], d["at"], d["text"]))


def find_e2(doc: plan.Doc, ctx: Ctx) -> list[Candidate]:
    """DESIGN 4.3 `find`: one candidate per (command, ordered string) pair, one per command that has a selector."""
    order = {t: i for i, t in enumerate(doc.tasks)}
    strings = _ordered_strings(doc, order)
    out: list[Candidate] = []
    for b in doc.of("criterion"):
        anchor = fnd.flat(b["text"])[:ANCHOR_MAX].rstrip()
        if len(anchor) < ANCHOR_MIN:
            continue
        upto = order.get(
            b["task"], len(order)
        )  # the goal belongs to no task: every task is earlier
        loc = {
            "task": b["task"],
            "line_start": b["line_start"],
            "line_end": b["line_end"],
        }
        seen: set[tuple[str, str, int]] = set()
        for span in _BACKTICKED.findall(b["text"]):
            cmd = _parse_command(span)
            if cmd is None:
                continue
            if cmd["kind"] == "selector":
                if (span, "", 0) in seen:
                    continue
                seen.add((span, "", 0))
                sel = {"k": cmd["k"], "m": cmd["m"], "id": cmd["id"]}
                out.append(
                    Candidate(
                        "E2", "C4", "selector", anchor, dict(loc),
                        features={
                            "no_match": 0, "near_miss": 0, "pattern_kind": "selector", "selector": sel,
                            "test_file": cmd["test_file"],
                        },
                        pre_priority=E2_BASE_PRIORITY,
                    )
                )  # fmt: skip
                continue
            for s in strings:
                if s["task"] > upto or (span, s["text"], s["line"]) in seen:
                    continue
                matched, kind = _literal_test(cmd, s["text"])
                near = matched is False and _collapse(cmd["pattern"]) == _collapse(
                    s["text"]
                )
                if not (
                    matched or near or _words_of(cmd["pattern"]) & _words_of(s["text"])
                ):
                    continue  # the string has nothing to do with this pattern
                seen.add((span, s["text"], s["line"]))
                no_match = int(matched is False)
                out.append(
                    Candidate(
                        "E2", "C4", "pattern", anchor, dict(loc),
                        features={
                            "no_match": no_match, "near_miss": int(near), "pattern_kind": kind,
                            "pattern": cmd["pattern"],
                            "case": "case-insensitive" if cmd["icase"] else "case-sensitive",
                            "string": s["text"], "string_line": s["line"], "noun": s["noun"],
                            "paths": cmd["paths"],
                        },
                        pre_priority=E2_BASE_PRIORITY + E2_NO_MATCH * no_match + E2_NEAR_MISS * int(near),
                    )
                )  # fmt: skip
    return out


def _parse_expr(expr: str):
    """A `-k` or `-m` expression (names, `and`, `or`, `not`, parentheses) as a tree; None when it does not parse."""
    toks = re.findall(r"\(|\)|[^\s()]+", expr)
    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else None

    def take():
        nonlocal pos
        pos += 1
        return toks[pos - 1]

    def p_or():
        node = p_and()
        while peek() == "or":
            take()
            node = ("or", node, p_and())
        return node

    def p_and():
        node = p_not()
        while peek() == "and":
            take()
            node = ("and", node, p_not())
        return node

    def p_not():
        t = peek()
        if t is None or t in (")", "and", "or"):
            raise ValueError(expr)
        if t == "not":
            take()
            return ("not", p_not())
        if t == "(":
            take()
            node = p_or()
            if peek() != ")":
                raise ValueError(expr)
            take()
            return node
        return ("id", take())

    try:
        tree = p_or()
        if pos != len(toks):
            raise ValueError(expr)
    except ValueError:
        return None
    return tree


def _run_expr(tree, holds) -> bool:
    op = tree[0]
    if op == "id":
        return holds(tree[1])
    if op == "not":
        return not _run_expr(tree[1], holds)
    left, right = _run_expr(tree[1], holds), _run_expr(tree[2], holds)
    return (left and right) if op == "and" else (left or right)


def _mark_names(node) -> set[str]:
    """Names of `pytest.mark.<name>` (or `mark.<name>`) in a decorator or a `pytestmark` value."""
    marks: set[str] = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Attribute):
            base = n.value
            if (isinstance(base, ast.Attribute) and base.attr == "mark") or (
                isinstance(base, ast.Name) and base.id == "mark"
            ):
                marks.add(n.attr)
    return marks


def _test_names(src: str, filename: str):
    """[(class or None, name, marker names)] of the test functions of a file; None when a Python file does not parse.

    Python files are read with `ast` (functions `test_*` and methods `test_*` of classes `Test*`); any other file
    by the `def test_` regex.
    """
    if not filename.endswith(".py"):
        return [(None, n, frozenset()) for n in re.findall(r"\bdef\s+(test_\w*)", src)]
    try:
        tree = ast.parse(src)
    except (SyntaxError, ValueError):
        return None
    module_marks: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets
        ):
            module_marks |= _mark_names(node.value)
    found = []
    funcs = (ast.FunctionDef, ast.AsyncFunctionDef)
    for node in tree.body:
        if isinstance(node, funcs) and node.name.startswith("test_"):
            marks = module_marks.union(*(_mark_names(d) for d in node.decorator_list))
            found.append((None, node.name, frozenset(marks)))
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            class_marks = module_marks.union(
                *(_mark_names(d) for d in node.decorator_list)
            )
            for sub in node.body:
                if isinstance(sub, funcs) and sub.name.startswith("test_"):
                    marks = class_marks.union(
                        *(_mark_names(d) for d in sub.decorator_list)
                    )
                    found.append((node.name, sub.name, frozenset(marks)))
    return found


def _count_selected(sel: dict, test_file: str, tests) -> int | None:
    """How many of `tests` the selector picks; None when an expression cannot be read."""
    k = _parse_expr(sel["k"]) if sel["k"] is not None else None
    m = _parse_expr(sel["m"]) if sel["m"] is not None else None
    if (sel["k"] is not None and k is None) or (sel["m"] is not None and m is None):
        return None
    ident = (
        [part.partition("[")[0] for part in sel["id"].split("::")]
        if sel["id"]
        else None
    )
    base = test_file.rpartition("/")[2]
    n = 0
    for cls, name, marks in tests:
        keys = [x.lower() for x in (name, cls, base, base.removesuffix(".py")) if x]
        if ident and not (
            (
                len(ident) == 1
                and ((cls is None and ident[0] == name) or ident[0] == cls)
            )
            or ident == [cls, name]
        ):
            continue  # `file::name` is a module-level test or a class; `file::Class::name` one method
        if k is not None and not _run_expr(
            k, lambda w, keys=keys: any(w.lower() in key for key in keys)
        ):
            continue
        if m is not None and not _run_expr(m, lambda w, marks=marks: w in marks):
            continue
        n += 1
    return n


def _read_in_snapshot(root: Path, rel: str) -> str | None:
    """A file of the snapshot as text, or None (missing, outside the snapshot, too large, or a ground-truth file)."""
    if GROUND_TRUTH_NAME.match(rel.rpartition("/")[2]):
        return None
    try:
        p = (root / rel).resolve()
        if (
            not p.is_relative_to(root)
            or not p.is_file()
            or p.stat().st_size > TEST_FILE_MAX
        ):
            return None
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _base_count(root: Path, term: str, paths: list[str]) -> int | None:
    """`git grep -c -F -e <term> -- <paths>` on the snapshot, summed over files; the DD-5 exclusions still apply."""
    excluded = [":(exclude,glob,icase)**/ground[-_]truth*"] + [
        f":(exclude,glob)**/{d}/**"
        for d in (DEV_DIR, *DEPENDENCY_DIRS)
        if not (
            d == DEV_DIR
            and any(p == DEV_DIR or p.startswith(DEV_DIR + "/") for p in paths)
        )
    ]
    argv = [
        "git",
        "-C",
        str(root),
        "grep",
        "-c",
        "-F",
        "-e",
        term,
        "--",
        *paths,
        *excluded,
    ]
    try:
        r = subprocess.run(argv, capture_output=True, env=_git_env(), timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode not in (0, 1):
        return None
    total = 0
    for line in r.stdout.decode("utf-8", "replace").splitlines():
        head, _, count = line.rpartition(":")
        total += int(count) if head and count.isdigit() else 0
    return total


def _selector_term(sel: dict) -> str | None:
    """The one bare name a selector asks for (for the base-checkout line), or None when it is an expression."""
    for raw in (
        sel["id"] and sel["id"].split("::")[-1].partition("[")[0],
        sel["k"],
        sel["m"],
    ):
        if raw and re.fullmatch(r"[\w.\-]+", raw) and raw not in ("and", "or", "not"):
            return raw
    return None


def _ev(path: str, line: int, text: str) -> dict:
    return {"path": path, "line": int(line), "text": text[:EVIDENCE_TEXT_MAX]}


def _shell_quote(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"


def attach_e2(cands: list[Candidate], ctx: Ctx) -> None:
    """DESIGN 4.3 `attach`: the evidence lines, then `priority`. A missing file or snapshot only drops that line."""
    root = git_root(ctx.snapshot) if ctx.snapshot is not None else None
    for c in cands:
        f = c.features
        ev: list[dict] = []
        zero = False
        if c.kind == "pattern":
            line, p, s = f["string_line"], f["pattern"], f["string"]
            ev.append(_ev("plan", line, f'the task orders the {f["noun"]} "{s}"'))
            if f["pattern_kind"] != "regex_unparsed":
                result = "NO MATCH" if f["no_match"] else "MATCH"
                ev.append(
                    _ev(
                        "plan",
                        line,
                        f"pattern '{p}' ({f['case']}) against ordered string '{s}': {result}",
                    )
                )
            if f["near_miss"]:
                ev.append(
                    _ev(
                        "plan",
                        line,
                        "after lowercasing and collapsing hyphens, spaces and underscores: MATCH",
                    )
                )
            term = p
        else:
            test_file = f["test_file"]
            src = (
                _read_in_snapshot(root, test_file)
                if root is not None and test_file
                else None
            )
            tests = _test_names(src, test_file) if src is not None else None
            n = (
                _count_selected(f["selector"], test_file, tests)
                if tests is not None
                else None
            )
            if n is not None:
                ev.append(
                    _ev(
                        test_file,
                        0,
                        f"{n} of {len(tests)} test names in {test_file} match the selector",
                    )
                )
                zero = n == 0
            term = _selector_term(f["selector"])
        paths = (
            f["paths"] if "paths" in f else [f["test_file"]] if f["test_file"] else []
        )
        if root is not None and term and "\n" not in term and paths:
            count = _base_count(root, term, paths)
            if count is not None:
                text = f"base checkout: git grep -c -F -e {_shell_quote(term)} -- {' '.join(paths)} gives {count}"
                ev.append(_ev(paths[0], 0, text))
        c.evidence = ev[:EVIDENCE_MAX]
        c.priority = min(100, c.pre_priority + (E2_SELECTOR_ZERO if zero else 0))


EXTRACTORS["E2"] = (find_e2, attach_e2)


# ---------------------------------------------------------------- E3 (class C8): files that refer to a file the plan edits
#
# DESIGN 4.4. Readings of the design that are not word for word (each is also in the report of Task 13):
#  - `find` checks that the target is present in the snapshot, as 4.4 requires ("existing means: present in the
#    snapshot"), by reading the snapshot's tracked-file list (`git ls-files`, no content search). Without a
#    snapshot nothing is present, so `find` returns no candidate. A snapshot that is not a git repository raises.
#  - Evidence holds at most 5 entries (DESIGN 4.1) and 4.4 asks for up to 5 referencing files plus the `gate names:`
#    line, which is 6. The limit of 4.1 is enforced by `Candidate.validate`, so at most 4 referencing files are
#    listed (tests first) and the gate line is the 5th entry. `unnamed_test_files` and `unnamed_other_files` still
#    count every such file, so `priority` does not depend on how many are listed.
#  - "The plan names a file" means its repo-relative path occurs as a path token in the plan text (the tokens of
#    `named_paths`). A bare file name is not a path token, and a folder token (`tests/`) does not name the files in
#    it. The same rule decides what the gate names: a gate that runs a whole folder names none of its files.
#  - The search helper keeps at most 3 hit lines per file, so a file whose first 3 hit lines hold only other
#    candidates' patterns can be missed for this one. The patterns are the same for every candidate of a call.
#  - `stem_hits` counts every file with a hit on the stem, the target file itself included (4.4: "all files, named
#    or not"). The listed and counted referencing files leave the target out.
#  - `has_distinctive`: a backticked word of the same sentence that is a plain identifier (letters, digits, `_`) and is
#    neither the target's file name nor its stem.
# The facts `attach_e3` needs travel in `Candidate.features` (`path`, `stem`), so a candidate read back from
# candidates.json can still be attached; the plan's named paths and gate come from `ctx.doc`.

E3_BASE_PRIORITY, E3_LONG_STEM, E3_DISTINCTIVE = 40, 10, 10
E3_LONG_STEM_LEN = 8
E3_TEST_WEIGHT, E3_TEST_CAP = 15, 3
E3_OTHER_WEIGHT, E3_OTHER_CAP = 5, 2
E3_GATE_NONE = 10
E3_COMMON_STEM_HITS, E3_COMMON_STEM_PENALTY = 40, 20
E3_FILES_MAX = EVIDENCE_MAX - 1  # one entry of the 5 is the `gate names:` line

_IDENTIFIER = re.compile(r"[A-Za-z_]\w*")
_TEST_PATH = re.compile(
    r"(?:^|/)(?:tests?|__tests__|specs?)/|(?:^|/)(?:test[_-][^/]*|conftest\.py|[^/]*[_.-](?:tests?|spec)\.\w+)$",
    re.IGNORECASE,
)


def find_e3(doc: plan.Doc, ctx: Ctx) -> list[Candidate]:
    """DESIGN 4.4 `find`: one candidate per edit target that exists in the snapshot (`creates` false)."""
    if ctx.snapshot is None:
        return []
    tracked = set(ctx.scope.tracked)
    out: list[Candidate] = []
    for b in doc.of("edit_target"):
        path = _clean_named(b.get("path") or "")
        if b.get("creates") or not path or path not in tracked:
            continue
        anchor = fnd.flat(b["text"])[:ANCHOR_MAX].rstrip()
        if len(anchor) < ANCHOR_MIN:
            continue
        base = path.rpartition("/")[2]
        stem = base.rpartition(".")[0] or base
        distinctive = any(
            _IDENTIFIER.fullmatch(s.strip()) and s.strip() not in (base, stem)
            for s in _BACKTICKED.findall(b["text"])
        )
        out.append(
            Candidate(
                "E3", "C8", "dependents", anchor,
                {"task": b["task"], "line_start": b["line_start"], "line_end": b["line_end"]},
                features={
                    "stem_len": len(stem), "has_distinctive": int(distinctive), "path": path, "stem": stem,
                },
                pre_priority=E3_BASE_PRIORITY
                + E3_LONG_STEM * (len(stem) >= E3_LONG_STEM_LEN)
                + E3_DISTINCTIVE * int(distinctive),
            )
        )  # fmt: skip
    return out


def _gate_names_text(names: list[str]) -> str:
    """`gate names: <paths or NONE>`, cut at a whole path so the evidence text limit never splits one."""
    head, shown = "gate names: ", []
    for i, n in enumerate(names):
        rest = len(names) - i - 1
        tail = f", and {rest} more" if rest else ""
        if shown and len(head + ", ".join(shown + [n]) + tail) > EVIDENCE_TEXT_MAX:
            return head + ", ".join(shown) + f", and {len(names) - i} more"
        shown.append(n)
    return head + (", ".join(shown) or "NONE")


def attach_e3(cands: list[Candidate], ctx: Ctx) -> None:
    """DESIGN 4.4 `attach`: one batched search for every target path and stem, then the evidence and `priority`.

    Without a snapshot there is nothing to search: no evidence, and `priority` is `pre_priority`.
    """
    if ctx.snapshot is None:
        for c in cands:
            c.evidence, c.priority = [], c.pre_priority
        return
    hits = search(
        ctx,
        sorted({p for c in cands for p in (c.features["path"], c.features["stem"])}),
    )
    named = set(ctx.named_paths)
    gates = ctx.doc.of("gate")
    gate_named = {
        _clean_named(m.group(0)) for g in gates for m in _PATH_TOKEN.finditer(g["text"])
    }
    gate_line = min((g["line_start"] for g in gates), default=0)
    for c in cands:
        path, stem = c.features["path"], c.features["stem"]
        first: dict[str, Hit] = {}  # referencing file -> its first hit line
        stem_files: set[str] = set()
        for h in hits:
            if stem in h.text:
                stem_files.add(h.path)
            if (path in h.text or stem in h.text) and h.path not in first:
                first[h.path] = h
        first.pop(path, None)  # the edited file is not one of its own dependents
        unnamed = sorted(f for f in first if f not in named)
        tests = [f for f in unnamed if _TEST_PATH.search(f)]
        others = [f for f in unnamed if not _TEST_PATH.search(f)]
        gate_files = sorted(f for f in first if f in gate_named)
        c.features.update(
            unnamed_test_files=len(tests),
            unnamed_other_files=len(others),
            stem_hits=len(stem_files),
        )
        c.evidence = [
            _ev(f, first[f].line, first[f].text.strip())
            for f in (tests + others)[:E3_FILES_MAX]
        ] + [_ev("plan", gate_line, _gate_names_text(gate_files))]
        c.priority = max(
            0,
            min(
                100,
                c.pre_priority
                + E3_TEST_WEIGHT * min(len(tests), E3_TEST_CAP)
                + E3_OTHER_WEIGHT * min(len(others), E3_OTHER_CAP)
                + E3_GATE_NONE * (not gate_files)
                - E3_COMMON_STEM_PENALTY * (len(stem_files) > E3_COMMON_STEM_HITS),
            ),
        )


EXTRACTORS["E3"] = (find_e3, attach_e3)


# ---------------------------------------------------------------- E4 (class C5): a count or "no remaining" claim
#
# DESIGN 4.5. Every place where this code narrows, widens or interprets 4.5 (each is also in the report of Task 14):
#  1. Evidence limit. 4.1 allows 5 evidence entries and 4.5 asks for up to 5 unnamed hits plus the `hits:` line, which
#     is 6. At most 4 unnamed hits are listed (one entry per file, its first hit line) and the `hits:` line is the 5th
#     entry. `unnamed_hits` and `unnamed_root_hits` still count every unnamed hit line, so `priority` does not depend
#     on how many are listed. The plan-named files are not listed one by one (the `hits:` line counts them): 4.5
#     "splits" hits into named and unnamed, and the split is shown as the `(<k> named by the plan)` count.
#  2. "Hit" is a hit line. The search helper (4.1) keeps at most 3 lines per file and reads 5,000 output lines, so `n` in
#     the `hits:` line is a floor, not an exact count. A hit belongs to a needle when the needle is a substring of the
#     stored hit line (the line is cut at HIT_TEXT_MAX after the helper's own test).
#  3. "Root-level document": a root-level file (no `/` in its path) with a documentation extension (E4_DOC_EXT), or a
#     root-level change-log style file. The `+20` of `unnamed_root_hits` counts only these. For the ORDER of the listed
#     hits, "root-level documents and change logs first" is read as: those root documents and the change-log style
#     files anywhere (DD-5 names); then same-basename mirrors of plan-named files; then the rest, each in path order.
#  4. "The plan names a file": the repo-relative path occurs as a path token in the plan (the tokens of `named_paths`),
#     as for E3, and in addition a root-level file of the scope whose bare name (`README.md`) occurs in the plan text,
#     because a path token needs a `/` and so can never name a root document.
#  5. Triggers. (a) A negative claim is a word of words.NEGATIVE_CLAIMS in one sentence with a backticked phrase; the
#     phrase nearest to the trigger is `needle`. A backticked span that is a command of the E2 families, a path token
#     or shorter than E4_NEEDLE_MIN characters is not a phrase. No phrase, no candidate. (b) A count change is
#     `[from] N [noun] to M [noun]` (needle: N and the first noun found, so "from 3 report formats to 4 report formats"
#     gives "3 report formats", the OLD value a stale place still carries), `N-member`, or `N noun`. A count change
#     with no noun anywhere is skipped (a bare digit is no search string). "N entries" is read as "a number followed
#     by a noun": the noun is the 1 or 2 words after the number up to the first word of words.NOT_NOUN. Numbers that
#     are part of a date, a version or a decimal, or that start with a zero before another digit (`007`: an id,
#     not a count), are no count. Backticked spans are code, so a number in one is no
#     count; the phrase of a negative claim may be backticked (a). A negative trigger such as "0 matches" is not read a
#     second time as a count.
#  6. Sentences. A block is split at blank lines first and then into sentences by the plan reader's `plan.sentences`,
#     so a line such as `Depends on: Task 1` is not glued to the next sentence. `goal` is a `criterion` block.
#     One candidate per (sentence line, needle, kind) so the same sentence in a `task` and a `criterion` block of a
#     documentation fixture is one item.
#  7. `anchor_text` is the sentence (first 200 characters, DESIGN 4.1); a sentence under 12 characters gives no item.
#  8. A priority from the formula of 4.5 is clamped to 0-100 like the other extractors. The `hits:` line is an entry
#     with path `plan` and the plan line of the sentence. Without a snapshot `attach` adds nothing.
# The facts `attach_e4` needs travel in `Candidate.features` (`needle`), so a candidate read back from candidates.json
# can still be attached.

E4_BASE_PRIORITY, E4_COUNT_CHANGE, E4_LONG_NEEDLE = 30, 10, 10
E4_ROOT_WEIGHT = 20
E4_UNNAMED_WEIGHT, E4_UNNAMED_CAP = 10, 3
E4_FILES_MAX = EVIDENCE_MAX - 1  # one entry of the 5 is the `hits:` line
E4_NEEDLE_MIN = 3
E4_NOUN_WORDS = 2
E4_DOC_EXT = (".md", ".markdown", ".rst", ".txt", ".adoc")

_NOT_NOUN = frozenset(words.NOT_NOUN)
_NEGATIVE = re.compile(
    r"(?<![\w-])(?:"
    + "|".join(
        re.escape(w).replace(r"\ ", r"[ \t]+")
        for w in sorted(words.NEGATIVE_CLAIMS, key=lambda w: (-len(w), w))
    )
    + r")(?![\w-])",
    re.IGNORECASE,
)
_NUM = r"(?<![\w.\-/$#])(?!0\d)\d+(?![\w\-/]|\.\d)"
_NOUNS_RE = r"[A-Za-z][A-Za-z\-]*(?:[ \t]+[A-Za-z][A-Za-z\-]*)?"
_COUNT_RANGE = re.compile(
    rf"(?:\bfrom[ \t]+)?(?P<a>{_NUM})(?:[ \t]+(?P<an>{_NOUNS_RE}))?[ \t]+to[ \t]+(?P<b>{_NUM})(?:[ \t]+(?P<bn>{_NOUNS_RE}))?",
    re.IGNORECASE,
)
_COUNT_MEMBER = re.compile(
    r"(?<![\w.\-/$#])(?!0\d)(?P<n>\d+)-members?(?![\w-])", re.IGNORECASE
)
_COUNT_NOUN = re.compile(rf"(?P<n>{_NUM})[ \t]+(?P<w>{_NOUNS_RE})", re.IGNORECASE)
_PARAGRAPH = re.compile(r"\S(?:[^\n]|\n(?![ \t]*\n))*")


def _noun(phrase: str | None) -> str:
    """The noun of a count: up to E4_NOUN_WORDS words of `phrase`, ended by the first word that cannot be a noun."""
    out: list[str] = []
    for w in (phrase or "").split():
        if w.lower() in _NOT_NOUN or len(out) == E4_NOUN_WORDS:
            break
        out.append(w)
    return " ".join(out)


def _overlaps(span: tuple[int, int], used: list[tuple[int, int]]) -> bool:
    return any(span[0] < z and a < span[1] for a, z in used)


def _e4_triggers(sent: str) -> list[tuple[int, str, str]]:
    """[(offset in the sentence, kind, needle)] of one sentence; kind is `negative` or `count`."""
    ticks = [
        (m.start(), m.end(), m.group(1).strip()) for m in _BACKTICKED.finditer(sent)
    ]
    masked = _BACKTICKED.sub(lambda m: " " * len(m.group(0)), sent)
    phrases = [
        (a, z, t)
        for a, z, t in ticks
        if len(t) >= E4_NEEDLE_MIN
        and _parse_command(t) is None
        and not re.fullmatch(formats.PATH_TOKEN, t)
    ]
    out: list[tuple[int, str, str]] = []
    used: list[tuple[int, int]] = []
    for m in _NEGATIVE.finditer(masked):
        used.append(m.span())

        def gap(p, m=m):
            return (max(p[0] - m.end(), m.start() - p[1], 0), p[0])

        near = min(phrases, key=gap, default=None)
        if near is not None:
            out.append((m.start(), "negative", near[2]))
    for m in _COUNT_RANGE.finditer(masked):
        if _overlaps(m.span(), used):
            continue
        used.append(m.span())
        noun = _noun(m["an"]) or _noun(m["bn"])
        if noun:
            out.append((m.start(), "count", f"{m['a']} {noun}"))
    for m in _COUNT_MEMBER.finditer(masked):
        if not _overlaps(m.span(), used):
            used.append(m.span())
            out.append((m.start(), "count", f"{m['n']}-member"))
    for m in _COUNT_NOUN.finditer(masked):
        noun = _noun(m["w"])
        if noun and not _overlaps(m.span(), used):
            used.append(m.span())
            out.append((m.start(), "count", f"{m['n']} {noun}"))
    return sorted(out)


def find_e4(doc: plan.Doc, ctx: Ctx) -> list[Candidate]:
    """DESIGN 4.5 `find`: one candidate per trigger in a `task` or `criterion` block (`goal` is a criterion)."""
    found: dict[tuple[int, str, str], tuple[int, Candidate]] = {}
    for b in doc.of("task", "criterion"):
        text = b["text"]
        for para in _PARAGRAPH.finditer(text):
            for start, _, sent in plan.sentences(para.group(0)):
                anchor = fnd.flat(sent)[:ANCHOR_MAX].rstrip()
                if len(anchor) < ANCHOR_MIN:
                    continue
                line = b["line_start"] + text.count("\n", 0, para.start() + start)
                for at, kind, needle in _e4_triggers(sent):
                    key = (line, needle, kind)
                    if key in found:
                        continue
                    count = int(kind == "count")
                    long_needle = int(
                        len(needle.split()) >= 2
                        or sum(c.isdigit() for c in needle) >= 2
                    )
                    found[key] = (
                        at,
                        Candidate(
                            "E4", "C5", kind, anchor,
                            {"task": b["task"], "line_start": line, "line_end": line + sent.count("\n")},
                            features={"needle": needle, "count_change": count, "long_needle": long_needle},
                            pre_priority=E4_BASE_PRIORITY + E4_COUNT_CHANGE * count + E4_LONG_NEEDLE * long_needle,
                        ),
                    )  # fmt: skip
    return [
        c
        for _, c in sorted(
            found.values(),
            key=lambda v: (v[1].location["line_start"], v[0], v[1].features["needle"]),
        )
    ]


def _e4_named(ctx: Ctx) -> set[str]:
    """Files the plan names: its path tokens, and root-level scope files whose bare name occurs in the plan text."""
    named = set(ctx.named_paths)
    for f in ctx.scope.files:
        if "/" not in f and re.search(
            r"(?<![\w/.\-])" + re.escape(f) + r"(?![\w\-/]|\.\w)", ctx.doc.text
        ):
            named.add(f)
    return named


def _is_root_doc(path: str) -> bool:
    return "/" not in path and (
        path.lower().endswith(E4_DOC_EXT) or bool(CHANGELOG_NAME.match(path))
    )


def _e4_group(path: str, mirrors: tuple[str, ...]) -> int:
    """0: root documents and change-log style files; 1: same-basename mirrors of plan-named files; 2: the rest."""
    base = path.rpartition("/")[2]
    if _is_root_doc(path) or CHANGELOG_NAME.match(base):
        return 0
    return 1 if base in mirrors else 2


def attach_e4(cands: list[Candidate], ctx: Ctx) -> None:
    """DESIGN 4.5 `attach`: one batched search for every needle, then the evidence and `priority`.

    Without a snapshot there is nothing to search: no evidence, and `priority` is `pre_priority`.
    """
    if ctx.snapshot is None:
        for c in cands:
            c.evidence, c.priority = [], c.pre_priority
        return
    hits = search(ctx, sorted({c.features["needle"] for c in cands}))
    named = _e4_named(ctx)
    mirrors = ctx.scope.mirrors
    for c in cands:
        mine = [h for h in hits if c.features["needle"] in h.text]
        unnamed = [h for h in mine if h.path not in named]
        root = sum(_is_root_doc(h.path) for h in unnamed)
        first: dict[str, Hit] = {}
        for h in unnamed:
            first.setdefault(h.path, h)
        listed = sorted(first, key=lambda f: (_e4_group(f, mirrors), f))[:E4_FILES_MAX]
        files = {h.path for h in mine}
        c.features.update(unnamed_root_hits=root, unnamed_hits=len(unnamed))
        c.evidence = [_ev(f, first[f].line, first[f].text.strip()) for f in listed] + [
            _ev(
                "plan",
                c.location["line_start"],
                f"hits: {len(mine)} in {len(files)} files ({len(files & named)} named by the plan)",
            )
        ]
        c.priority = max(
            0,
            min(
                100,
                c.pre_priority
                + E4_ROOT_WEIGHT * (root > 0)
                + E4_UNNAMED_WEIGHT * min(len(unnamed), E4_UNNAMED_CAP),
            ),
        )


EXTRACTORS["E4"] = (find_e4, attach_e4)


# ---------------------------------------------------------------- E1 (classes C1 and C6): set words and their scope
#
# DESIGN 4.2. Every place where this code narrows, widens or interprets 4.2 (each is also in the report of Task 15):
#  1. Evidence limit. 4.1 allows 5 evidence entries; 4.2 asks `universal` for up to 3 plan limiter lines, the enforcing
#     test, up to 3 limiter lines of its file and the `def test_` count, which is 8. The order is: plan limiter lines,
#     the enforcing-test line, the `def test_` count (only when the file is in the snapshot), then limiter lines of the
#     file. The enforcing-test line and the count are kept; the other 3 (or more) slots go to plan lines first, but a
#     file with limiter lines always gets at least 1 of them (so 2 plan lines and 1 file line when both have 3).
#     `limiter_lines` (the count of ALL plan limiter lines) drives `priority`, not the number shown.
#  2. Sentences. A block is split at blank lines and at list bullets (a line that starts with `-`, `*`, `+` or `1.`),
#     then by `plan.sentences`; the bullet marker is not part of the sentence. A sentence needs 12 characters after
#     `fnd.flat` (the anchor); the anchor is its first 200 characters. `goal` is a criterion block.
#  3. Set words are matched in the sentence as written, backticked spans included. `set_word_count` counts matches
#     (a word twice is 2). The pair `outside ... nothing` counts once when `outside` comes before `nothing`. A sentence
#     with both kinds of word gives one candidate of each kind (same anchor, two classes).
#  4. Tokens. A path token is `formats.PATH_TOKEN` without `*`; a glob token has a `*` (with a `/`, or a bare name with
#     an extension such as `*.py`); a test token is a bare `test_*.py` file name (no `*`). `instr_scope` and
#     `sent_scope` hold path and glob tokens only, as sorted sets. Bound type is tested in the order the table lists
#     them: `closed_list` (2 or more distinct path tokens and no glob), `glob` (any glob), `count` (a number and a noun
#     of E4, backticked text left out), else `none`. `names_path` is true for any path, glob or test token.
#  5. Scopes. `instr_scope` is the union over the whole `task` block (the text before `Acceptance criteria:`) of the
#     task the sentence is in; a sentence in no task (the goal) has an empty `instr_scope`. The plan line shown for it
#     is the first line of the first sentence of that body that names a token (the task heading line when none does).
#  6. `universal` limiter lines are whole plan lines that contain a token of the sentence (as a plain substring, a glob
#     included) and a limiter word; the lines of the sentence itself are left out. A line longer than 160 characters
#     is shown as the sentence of that line that holds the first limiter word (the text limit would cut the limiter).
#  7. The enforcing test is the FIRST test file named in the criteria of the sentence's task (the sentence's own
#     criterion included) and then in the gate blocks: a path token whose base name is `test_*.py` or whose path
#     starts with `tests/` or holds `/tests/` (a folder token does not count), or a bare `test_*.py` name. A glob is not a file. "Enforcing
#     test file found" in `priority` means the PLAN names one; whether the file is in the snapshot only decides the
#     evidence of the file. A bare name is looked up in the snapshot's tracked files and is used when exactly one
#     tracked file has that base name. Without a snapshot there is no file evidence.
# The facts `attach_e1` needs travel in `Candidate.features`, so a candidate read back from candidates.json can still
# be attached; the plan's own lines come from `ctx.doc`. `route` is copied from the class card here (C1 read, C6 search).

E1_BASE, E1_BOUND_NONE, E1_SCOPE_DIFFERS = 30, 25, 25
E1_EXTRA_WORD, E1_EXTRA_CAP = 5, 2
E1_NAMES_PATH = 20
E1_LIMITER, E1_TEST = 20, 20
E1_LIMITER_LINES = 3
E1_NONE = "NONE"


def _words_re(spec) -> re.Pattern:
    alts = sorted({w.lower() for w in spec}, key=lambda w: (-len(w), w))
    body = "|".join(re.escape(w).replace(r"\ ", r"[ \t]+") for w in alts)
    return re.compile(rf"(?<![\w-])(?:{body})(?![\w-])", re.IGNORECASE)


_SET_COMPLETE = _words_re(words.SET_COMPLETENESS)
_SET_UNIVERSAL = _words_re(words.SET_UNIVERSAL)
_SET_PAIRS = tuple(
    (_words_re((a,)), _words_re((b,))) for a, b in words.SET_UNIVERSAL_PAIRS
)
_LIMITER_RE = _words_re(words.LIMITERS)
_GLOB_BARE = re.compile(r"(?<![\w/.\-*])[\w\-]*\*[\w\-]*\.[A-Za-z0-9*]+(?![\w/])")
_TEST_BARE = re.compile(r"(?<![\w/.\-*])test_[\w\-]*\.py(?![\w/])")
_BULLET_LINE = re.compile(r"[ \t]*(?:[-*+]|\d+[.)])[ \t]+")


def _e1_sentences(text: str) -> list[tuple[int, str]]:
    """[(offset in text, sentence)]: the block split at blank lines and list bullets, then at sentence ends."""
    out: list[tuple[int, str]] = []
    seg: int | None = None
    pos = 0

    def close(end: int) -> None:
        if seg is not None:
            out.extend((seg + s, sent) for s, _, sent in plan.sentences(text[seg:end]))

    for raw in text.split("\n"):
        if not raw.strip():
            close(pos)
            seg = None
        elif m := _BULLET_LINE.match(raw):
            close(pos)
            seg = pos + m.end()
        elif seg is None:
            seg = pos + len(raw) - len(raw.lstrip())
        pos += len(raw) + 1
    close(len(text))
    return out


def _e1_tokens(text: str) -> list[tuple[int, str, str]]:
    """[(offset, kind, token)] in text order; kind is `path`, `glob` or `test` (a bare test_*.py file name)."""
    found = [
        (m.start(), "glob" if "*" in m.group(0) else "path", m.group(0))
        for m in _PATH_TOKEN.finditer(text)
    ]
    found += [(m.start(), "glob", m.group(0)) for m in _GLOB_BARE.finditer(text)]
    found += [(m.start(), "test", m.group(0)) for m in _TEST_BARE.finditer(text)]
    return sorted(found)


def _scope_of(tokens) -> list[str]:
    return sorted({t for _, k, t in tokens if k in ("path", "glob")})


def _bound_type(sent: str, tokens) -> str:
    paths = {t for _, k, t in tokens if k == "path"}
    if any(k == "glob" for _, k, _ in tokens):
        return "glob"
    if len(paths) >= 2:
        return "closed_list"
    masked = _BACKTICKED.sub(lambda m: " " * len(m.group(0)), sent)
    if any(_noun(m["w"]) for m in _COUNT_NOUN.finditer(masked)):
        return "count"
    return "none"


def _is_test_file(kind: str, tok: str) -> bool:
    if kind == "test":
        return True
    base = tok.rpartition("/")[2]
    return (
        kind == "path"
        and not tok.endswith("/")
        and (
            bool(re.fullmatch(r"test_.*\.py", base))
            or tok.startswith("tests/")
            or "/tests/" in tok
        )
    )


def _enforcing_test(doc: plan.Doc, task: str) -> tuple[str | None, int | None]:
    """(path or name, plan line) of the first test file named in the task's criteria, then in the gate."""
    blocks = [b for b in doc.of("criterion") if b["task"] == task] + doc.of("gate")
    for b in blocks:
        for at, kind, tok in _e1_tokens(b["text"]):
            name = _clean_named(tok) if _is_test_file(kind, tok) else None
            if name:
                return name, b["line_start"] + b["text"].count("\n", 0, at)
    return None, None


def _task_scopes(doc: plan.Doc) -> dict[str, tuple[list[str], int]]:
    """{task: (instr_scope, plan line of the first sentence of the task body that names a token)}."""
    out: dict[str, tuple[list[str], int]] = {}
    for b in doc.of("task"):
        text = b["text"]
        scope = _scope_of(_e1_tokens(text))
        line = next(
            (
                b["line_start"] + text.count("\n", 0, s)
                for s, _, sent in plan.sentences(text)
                if _scope_of(_e1_tokens(sent))
            ),
            doc.tasks.get(b["task"], {}).get("line") or b["line_start"],
        )
        out[b["task"]] = (scope, line)
    return out


def find_e1(doc: plan.Doc, ctx: Ctx) -> list[Candidate]:
    """DESIGN 4.2 `find`: a candidate of kind `completeness` (C1) or `universal` (C6) per sentence with a set word."""
    routes = cards.routes()
    scopes = _task_scopes(doc)
    found: dict[tuple[int, str, str], Candidate] = {}
    for b in doc.of("criterion", "dictated_text"):
        text = b["text"]
        for at, sent in _e1_sentences(text):
            anchor = fnd.flat(sent)[:ANCHOR_MAX].rstrip()
            if len(anchor) < ANCHOR_MIN:
                continue
            line = b["line_start"] + text.count("\n", 0, at)
            loc = {
                "task": b["task"],
                "line_start": line,
                "line_end": line + sent.count("\n"),
            }
            tokens = _e1_tokens(sent)
            n_complete = len(_SET_COMPLETE.findall(sent))
            n_universal = len(_SET_UNIVERSAL.findall(sent))
            for first, second in _SET_PAIRS:
                m = first.search(sent)
                n_universal += bool(m and second.search(sent, m.end()))
            if n_complete and (line, "completeness", anchor) not in found:
                instr, instr_line = scopes.get(b["task"], ([], None))
                sent_scope = _scope_of(tokens)
                bound = _bound_type(sent, tokens)
                bound_none = int(bound in ("none", "glob"))
                differs = int(bool(instr) and bool(sent_scope) and instr != sent_scope)
                found[(line, "completeness", anchor)] = Candidate(
                    "E1", "C1", "completeness", anchor, dict(loc),
                    features={
                        "bound_none": bound_none, "scope_differs": differs, "set_word_count": n_complete,
                        "bound": bound, "instr_scope": instr, "sent_scope": sent_scope, "instr_line": instr_line,
                    },
                    pre_priority=E1_BASE
                    + E1_BOUND_NONE * bound_none
                    + E1_SCOPE_DIFFERS * differs
                    + E1_EXTRA_WORD * min(n_complete - 1, E1_EXTRA_CAP),
                    route=routes["C1"],
                )  # fmt: skip
            if n_universal and (line, "universal", anchor) not in found:
                names = [t for _, _, t in tokens]
                test, test_line = _enforcing_test(doc, b["task"])
                found[(line, "universal", anchor)] = Candidate(
                    "E1", "C6", "universal", anchor, dict(loc),
                    features={
                        "names_path": int(bool(names)), "set_word_count": n_universal,
                        "tokens": list(dict.fromkeys(names)), "enforcing_test": test, "enforcing_test_line": test_line,
                    },
                    pre_priority=E1_BASE
                    + E1_NAMES_PATH * int(bool(names))
                    + E1_EXTRA_WORD * min(n_universal - 1, E1_EXTRA_CAP),
                    route=routes["C6"],
                )  # fmt: skip
    return sorted(
        found.values(), key=lambda c: (c.location["line_start"], c.kind, c.anchor_text)
    )


def _scope_text(prefix: str, tokens: list[str], suffix: str = "") -> str:
    """`<prefix>[a, b]<suffix>` (`[NONE]` when empty), with whole tokens dropped (`and N more`) to fit the limit."""
    shown = list(tokens)
    while True:
        more = len(tokens) - len(shown)
        inner = ", ".join(shown + ([f"and {more} more"] if more else [])) or E1_NONE
        text = f"{prefix}[{inner}]{suffix}"
        if len(text) <= EVIDENCE_TEXT_MAX or not shown:
            return text
        shown.pop()


def _quote_line(line: str) -> str:
    """The line, stripped; a line over the text limit is shown as its sentence that holds the first limiter word."""
    line = line.strip()
    if len(line) <= EVIDENCE_TEXT_MAX:
        return line
    m = _LIMITER_RE.search(line)
    for s, e, sent in plan.sentences(line):
        if m and s <= m.start() < e:
            return sent
    return line


def _limiter_lines(
    lines: list[str], tokens: list[str], skip: tuple[int, int]
) -> list[tuple[int, str]]:
    """[(line number, text)] of the lines (outside `skip`) that hold a token and a limiter word, in order."""
    return [
        (i, _quote_line(line))
        for i, line in enumerate(lines, 1)
        if not skip[0] <= i <= skip[1]
        and _LIMITER_RE.search(line)
        and any(t in line for t in tokens)
    ]


def _snapshot_file(
    ctx: Ctx, root: Path, name: str
) -> tuple[str, str] | tuple[None, None]:
    """(repo-relative path, text) of the named test file in the snapshot, or (None, None)."""
    text = _read_in_snapshot(root, name)
    if text is not None:
        return name, text
    if "/" not in name:
        same = [f for f in ctx.scope.tracked if f.endswith("/" + name)]
        text = _read_in_snapshot(root, same[0]) if len(same) == 1 else None
        if text is not None:
            return same[0], text
    return None, None


def attach_e1(cands: list[Candidate], ctx: Ctx) -> None:
    """DESIGN 4.2 `attach`: both scopes side by side (`completeness`), or limiter lines and the enforcing test."""
    root = git_root(ctx.snapshot) if ctx.snapshot is not None else None
    for c in cands:
        f, loc = c.features, c.location
        if c.kind == "completeness":
            c.evidence = [
                _ev("plan", f["instr_line"] or loc["line_start"], _scope_text("instruction scope: ", f["instr_scope"])),
                _ev("plan", loc["line_start"], _scope_text("criterion scope: ", f["sent_scope"], f", bound: {f['bound']}")),
            ]  # fmt: skip
            c.priority = c.pre_priority
            continue
        plan_ev = [
            _ev("plan", n, t)
            for n, t in _limiter_lines(
                ctx.doc.lines, f["tokens"], (loc["line_start"], loc["line_end"])
            )
        ]
        fixed: list[dict] = []
        file_ev: list[dict] = []
        test, defs = f["enforcing_test"], None
        if test:
            note = ""
            rel = src = None
            if root is not None:
                rel, src = _snapshot_file(ctx, root, test)
                note = "" if src is not None else " (not in the snapshot)"
            fixed.append(
                _ev(
                    "plan",
                    f["enforcing_test_line"],
                    f"enforcing test named by the plan: {test}{note}",
                )
            )
            if src is not None:
                defs = len(re.findall(r"\bdef\s+test_", src))
                fixed.append(_ev(rel, 0, f"{defs} def test_ functions in {rel}"))
                file_ev = [
                    _ev(rel, n, _quote_line(line))
                    for n, line in enumerate(src.split("\n"), 1)
                    if _LIMITER_RE.search(line)
                ][:E1_LIMITER_LINES]  # fmt: skip
        free = EVIDENCE_MAX - len(fixed)
        take_plan = min(len(plan_ev), E1_LIMITER_LINES, free - (1 if file_ev else 0))
        take_file = min(len(file_ev), free - take_plan)
        c.evidence = plan_ev[:take_plan] + fixed + file_ev[:take_file]
        c.features.update(limiter_lines=len(plan_ev), test_defs=defs)
        c.priority = max(
            0,
            min(
                100, c.pre_priority + E1_LIMITER * bool(plan_ev) + E1_TEST * bool(test)
            ),
        )


EXTRACTORS["E1"] = (find_e1, attach_e1)


# ---------------------------------------------------------------- E5 (class C2): source rules a citing task leaves out
#
# DESIGN 4.6. Runs only when a source exists (`ctx.source`); without one `find_e5` returns nothing and `Ctx.no_source`
# / `Ctx.not_applicable` say class C2 is not applicable. `find_e5` reads only the candidate and the source (no
# repository access); `attach_e5` builds the three evidence entries from `Candidate.features`, so a candidate read
# back from candidates.json can still be attached. Reading choices where DESIGN 4.6 is silent:
#  1. The source is split at its markdown headings, whatever its format dictionary. A numeric citation (`2.3`) names
#     the heading whose title starts with that number (`2.3` does not match `2.30` or `2.3.1`); its section runs to the
#     next heading of the same or a higher level, so sub-sections belong to it. A citation that starts with a letter
#     (`Q4`) names a heading that starts with it, or else a decision line that starts with it (`Q4: ...`, also as a
#     bullet or in bold) and runs to the next blank line, bullet, heading or other decision line. `§` and `section` are
#     dropped by the plan reader's citation pattern. A citation that matches nothing gives no rules.
#  2. Prose only: heading lines and fenced lines of the source are no rule sentences. A new paragraph starts at a blank
#     line, a bullet, a heading or a fence; sentences are cut by `plan.sentences`.
#  3. "Next to" in the second rule clause is read as "in the same sentence": a sentence with a backticked span and one
#     of the verbs report, return, halt, set, write (any inflection) is a rule sentence. The first clause is the words
#     must, shall, never, always, only, every, each.
#  4. `ids` are the backticked spans without a space (at most 80 characters) and, outside backticks, the snake_case
#     tokens (a lower-case word with an underscore) and the CamelCase tokens (two humps, at least one lower-case
#     letter; `DoorTimeout`, `doorTimeout`; an all-capital word is none). Duplicates are kept once, in order.
#  5. The task text searched is the task block and its criterion blocks, whitespace-flattened; an id is found when it
#     is a substring (case-sensitive). The citation line is part of the task block and holds no identifier.
#  6. The task's first sentence is the first sentence of 12 or more characters in the task body, outside the citation
#     line and a `Depends on:` line (each breaks a paragraph and is no sentence), cut to 200 characters like E4. A task
#     without such a sentence gives no candidate. Its location is that sentence's.
#  7. A task is counted in `ctx.tasks_without_citations` when the plan reader found no citation for it, whether or not
#     the source has a rule for the others. Two rule sentences of one task are two candidates with the same anchor.
#  8. Evidence is three entries (the limit is 5): the rule (`source`, its source line), `missing identifiers: <list>`
#     (`source`, the same line) and the task's first sentence (`plan`, its plan line); each text is cut to 160.

E5_BASE_PRIORITY, E5_PER_MISSING, E5_MISSING_CAP = 30, 15, 4
E5_ID_MAX = 80
_E5_MODAL = re.compile(
    r"(?<![\w-])(?:must|shall|never|always|only|every|each)(?![\w-])", re.I
)
_E5_VERB = re.compile(
    r"(?<![\w-])(?:reports?|reported|reporting|returns?|returned|returning|halts?|halted|halting|sets?|setting"
    r"|writes?|wrote|written|writing)(?![\w-])",
    re.I,
)
_E5_FENCE = re.compile(r"^ {0,3}(?:`{3,}|~{3,})")
_E5_HEAD = re.compile(r"^(#{1,6})[ \t]+(\S.*?)[ \t]*#*[ \t]*$")
_E5_BULLET = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]+")
_E5_DECISION_ANY = re.compile(
    r"^[ \t]*(?:[-*+][ \t]+)?(?:\*\*)?[A-Z]{1,3}-?\d+(?:\.\d+)*(?:\*\*)?[ \t]*[:.)]"
)
_E5_SNAKE = re.compile(r"(?<![\w-])[a-z][a-z0-9]*(?:_[a-z0-9]+)+(?![\w-])")
_E5_CAMEL = re.compile(r"(?<![\w-])[A-Z]?[a-z][a-z0-9]*(?:[A-Z][a-z0-9]+)+(?![\w-])")
_E5_TICKED = re.compile(r"`([^`\n]+)`")
_E5_DEPENDS = re.compile(r"^[ \t]*Depends on[ \t]*:", re.I)


def _e5_prose(lines: list[str], lo: int, hi: int):
    """(line number, text) for the prose lines lo..hi of a document (1-based): fenced lines and headings are left
    out, and a None entry stands for a break (a fence or a heading). Blank lines are kept as ''."""
    fenced = False
    out: list[tuple[int, str] | None] = []
    for i in range(1, hi + 1):
        raw = lines[i - 1]
        if _E5_FENCE.match(raw):
            fenced = not fenced
            if i >= lo:
                out.append(None)
            continue
        if fenced or i < lo:
            continue
        out.append(None if _E5_HEAD.match(raw) else (i, raw))
    return out


def _e5_heads(lines: list[str]) -> list[dict]:
    """The headings of a document outside fences: {line, level, title, end} with `end` the last line of the section."""
    heads, fenced = [], False
    for i, raw in enumerate(lines, 1):
        if _E5_FENCE.match(raw):
            fenced = not fenced
            continue
        m = None if fenced else _E5_HEAD.match(raw)
        if m:
            heads.append({"line": i, "level": len(m.group(1)), "title": m.group(2)})
    for k, h in enumerate(heads):
        h["end"] = len(lines)
        for g in heads[k + 1 :]:
            if g["level"] <= h["level"]:
                h["end"] = g["line"] - 1
                break
    return heads


def _e5_ranges(
    lines: list[str], heads: list[dict], ref: str
) -> list[tuple[int, int, str]]:
    """The (first line, last line, kind) ranges of the source that the citation `ref` names (reading choice 1)."""
    head_rx = re.compile(rf"(?:§\s*)?{re.escape(ref)}(?![\w])(?!\.\d)")
    out = [
        (h["line"] + 1, h["end"], "section") for h in heads if head_rx.match(h["title"])
    ]
    if out or not ref[0].isalpha():
        return out
    dec_rx = re.compile(
        rf"^[ \t]*(?:[-*+][ \t]+)?(?:\*\*)?{re.escape(ref)}(?:\*\*)?[ \t]*[:.)]"
    )
    fenced = False
    for i, raw in enumerate(lines, 1):
        if _E5_FENCE.match(raw):
            fenced = not fenced
            continue
        if fenced or _E5_HEAD.match(raw) or not dec_rx.match(raw):
            continue
        j = i
        while j < len(lines):
            nxt = lines[j]
            if (
                not nxt.strip()
                or _E5_HEAD.match(nxt)
                or _E5_BULLET.match(nxt)
                or _E5_DECISION_ANY.match(nxt)
            ):
                break
            j += 1
        out.append((i, j, "decision"))
    return out


def _e5_paragraphs(lines: list[str], lo: int, hi: int):
    """(first line, text) of each prose paragraph of lines lo..hi (reading choice 2)."""
    para: list[tuple[int, str]] = []
    for item in [*_e5_prose(lines, lo, hi), None]:
        if item is not None and item[1].strip() and not _E5_BULLET.match(item[1]):
            para.append(item)
            continue
        if para:
            yield para[0][0], "\n".join(t for _, t in para)
            para = []
        if item is not None and item[1].strip():  # a bullet starts a new paragraph
            para = [item]


def _e5_is_rule(sentence: str) -> bool:
    ticked = _E5_TICKED.search(sentence) is not None
    return bool(_E5_MODAL.search(sentence) or (ticked and _E5_VERB.search(sentence)))


def _e5_rules(lines: list[str], lo: int, hi: int) -> list[tuple[int, str]]:
    """(source line, flattened sentence) of every rule sentence in lines lo..hi."""
    out = []
    for first, text in _e5_paragraphs(lines, lo, hi):
        for start, _, sent in plan.sentences(text):
            flat = fnd.flat(_E5_BULLET.sub("", sent, count=1))
            if _e5_is_rule(flat):
                out.append((first + text.count("\n", 0, start), flat))
    return out


def _e5_ids(sentence: str) -> list[str]:
    """The identifiers of a rule sentence (reading choice 4), each once, in order of appearance."""
    found = [(m.start(1), m.group(1).strip()) for m in _E5_TICKED.finditer(sentence)]
    bare = _E5_TICKED.sub(lambda m: " " * len(m.group(0)), sentence)
    for rx in (_E5_SNAKE, _E5_CAMEL):
        found += [(m.start(), m.group(0)) for m in rx.finditer(bare)]
    seen: list[str] = []
    for _, tok in sorted(found):
        if (
            tok
            and len(tok) <= E5_ID_MAX
            and not any(c.isspace() for c in tok)
            and tok not in seen
        ):
            seen.append(tok)
    return seen


def _e5_first_sentence(doc: plan.Doc, block: dict) -> tuple[int, str] | None:
    """(plan line, text) of the first sentence of 12 or more characters in a task block (reading choice 6)."""
    spec = formats.FORMATS.get(doc.format) or {}
    label = re.compile((spec.get("citation") or formats.CITATION)["label"], re.I)
    para: list[tuple[int, str]] = []
    for n, raw in [*enumerate(block["text"].split("\n"), block["line_start"]), (0, "")]:
        if raw.strip() and not label.match(raw) and not _E5_DEPENDS.match(raw):
            para.append((n, raw))
            continue
        if para:
            text = "\n".join(t for _, t in para)
            for start, _, sent in plan.sentences(text):
                if len(fnd.flat(sent)) >= ANCHOR_MIN:
                    return para[0][0] + text.count("\n", 0, start), sent
            para = []
    return None


def find_e5(doc: plan.Doc, ctx: Ctx) -> list[Candidate]:
    """DESIGN 4.6 `find`: one candidate per (task, rule sentence of a cited section) with identifiers the task lacks."""
    ctx.tasks_without_citations = []
    source = ctx.source
    if source is None:
        return []
    heads = _e5_heads(source.lines)
    out: list[Candidate] = []
    for tid, task in doc.tasks.items():
        refs = task["citations"]
        if not refs:
            ctx.tasks_without_citations.append(tid)
            continue
        block = next((b for b in doc.of("task") if b["task"] == tid), None)
        first = _e5_first_sentence(doc, block) if block else None
        if first is None:
            continue
        line, sent = first
        haystack = fnd.flat(
            "\n".join(
                b["text"] for b in doc.of("task", "criterion") if b["task"] == tid
            )
        )
        anchor = fnd.flat(sent)[:ANCHOR_MAX].rstrip()
        done: set[tuple[int, str]] = set()
        for ref in refs:
            for lo, hi, kind in _e5_ranges(source.lines, heads, ref):
                for rule_line, rule in _e5_rules(source.lines, lo, hi):
                    ids = _e5_ids(rule)
                    missing = [i for i in ids if i not in haystack]
                    if not missing or (rule_line, rule) in done:
                        continue
                    done.add((rule_line, rule))
                    out.append(
                        Candidate(
                            "E5", "C2", kind, anchor,
                            {"task": tid, "line_start": line, "line_end": line + sent.count("\n")},
                            features={"ref": ref, "rule": rule, "rule_line": rule_line, "ids": ids,
                                      "missing": missing, "task_sentence": fnd.flat(sent)},
                            pre_priority=E5_BASE_PRIORITY + E5_PER_MISSING * min(len(missing), E5_MISSING_CAP),
                        )
                    )  # fmt: skip
    return out


def attach_e5(cands: list[Candidate], ctx: Ctx) -> None:
    """DESIGN 4.6 `attach`: the rule, the missing identifiers and the task's first sentence; `priority = pre_priority`."""
    for c in cands:
        f = c.features
        c.evidence = [
            _ev("source", f["rule_line"], f["rule"]),
            _ev(
                "source",
                f["rule_line"],
                "missing identifiers: " + ", ".join(f["missing"]),
            ),
            _ev("plan", c.location["line_start"], f["task_sentence"]),
        ]
        c.priority = c.pre_priority


EXTRACTORS["E5"] = (find_e5, attach_e5)


# ---------------------------------------------------------------- E7 (class C7): constraint clauses dictated text omits
#
# DESIGN 4.8. Lexical only: `find_e7` makes the whole grid and keeps it in `features`; `attach_e7` writes the evidence.

E7_BASE_PRIORITY, E7_ZERO_WEIGHT, E7_ZERO_CAP, E7_SHARED_WEIGHT = 30, 15, 2, 10
E7_CLAUSE_MIN_WORDS, E7_TOKEN_MIN, E7_SHARED_MIN = 4, 4, 2
E7_CLAUSE_TEXT_MAX = 100
_E7_STOP = frozenset(words.STOP)
_E7_SPLIT = re.compile(r";|,| and ")
_E7_TOKEN = re.compile(r"[a-z0-9_]+")


def _e7_tokens(text: str) -> set[str]:
    return {
        t
        for t in _E7_TOKEN.findall(text.lower())
        if len(t) >= E7_TOKEN_MIN and t not in _E7_STOP
    }


def _e7_clauses(block: dict) -> list[tuple[int, str]]:
    """(plan line, flattened clause) of each clause of 4 or more words of a constraint block, in order."""
    # [first line, raw text] per bullet or paragraph of the block
    items: list[list] = []
    for n, raw in enumerate(block["text"].split("\n"), block["line_start"]):
        if not raw.strip():
            items.append([n, ""])
        elif items and items[-1][1] and not _E5_BULLET.match(raw):
            items[-1][1] += "\n" + raw
        else:
            items.append([n, _E5_BULLET.sub("", raw, count=1)])
    out = []
    for first, text in items:
        for start, _, sent in plan.sentences(text):
            line = first + text.count("\n", 0, start)
            for part in _E7_SPLIT.split(fnd.flat(sent)):
                part = part.strip()
                if len(part.split()) >= E7_CLAUSE_MIN_WORDS:
                    out.append((line, part))
    return out


def _e7_anchor(block: dict, ctx: Ctx) -> tuple[int, str, int] | None:
    """(plan line, anchor, last line) of the first sentence of 12 or more characters of a dictated block, cut to 200
    characters; when its text is not a quote of the plan (a quoted sentence that wraps over `> ` lines), its first
    line is used instead."""
    text = block["text"]
    for start, _, sent in plan.sentences(text):
        for part in (sent, sent.split("\n")[0]):
            anchor = fnd.flat(part)[:ANCHOR_MAX].rstrip()
            if len(anchor) >= ANCHOR_MIN and anchor in ctx.flat_text:
                line = block["line_start"] + text.count("\n", 0, start)
                return line, anchor, line + part.count("\n")
        if len(fnd.flat(sent)) >= ANCHOR_MIN:
            return None
    return None


# Where I narrowed or interpreted DESIGN 4.8 (each is also in the Task 17 report):
#  1. A "word" is a run of [a-z0-9_] after lower-casing, so a number such as 2027 can be a distinctive token and a
#     hyphenated or dotted name is several words; a token matches whole, with no stemming ("expiry" is not "expired").
#  2. A constraint block is read as bullets and paragraphs, and each sentence of one is split at ";", "," and " and "
#     (a line break or a sentence end is also a clause boundary, which 4.8 does not say; a block can hold several).
#  3. A zero-overlap clause must hold at least one distinctive token (a clause with none is the blind spot of 4.8, so it
#     proves nothing); the "one clause" with 2 or more shared tokens is the one with the most, earliest on a tie.
#  4. The "first sentence" of a dictated block is its first sentence of 12 or more characters; one that is not an
#     exact quote of the plan falls back to its first line, and a block with no such text makes no candidate.
#  5. With more than 5 clauses the evidence keeps the sharing clause, up to 2 zero-overlap clauses, then the earliest.
def find_e7(doc: plan.Doc, ctx: Ctx) -> list[Candidate]:
    """DESIGN 4.8 `find`: one candidate per (constraint, dictated block) that shares tokens with one clause only."""
    out: list[Candidate] = []
    anchors: dict[int, tuple | None] = {}
    for con in doc.of("constraint"):
        clauses = _e7_clauses(con)
        toks = [_e7_tokens(text) for _, text in clauses]
        distinct = [
            {t for t in tk if sum(t in other for other in toks) == 1} for tk in toks
        ]
        if len(clauses) < 2:
            continue
        for i, blk in enumerate(doc.of("dictated_text")):
            block_toks = _e7_tokens(blk["text"])
            shared = [sorted(d & block_toks) for d in distinct]
            best = max(range(len(shared)), key=lambda k: (len(shared[k]), -k))
            zero = [k for k, d in enumerate(distinct) if d and not shared[k]]
            if len(shared[best]) < E7_SHARED_MIN or not zero:
                continue
            if i not in anchors:
                anchors[i] = _e7_anchor(blk, ctx)
            if anchors[i] is None:
                continue
            line, anchor, end = anchors[i]
            out.append(
                Candidate(
                    "E7", "C7", "clause", anchor,
                    {"task": blk["task"], "line_start": line, "line_end": end},
                    features={
                        "constraint": con["id"], "constraint_line": con["line_start"],
                        "best": best, "zero": zero,
                        "clauses": [
                            {"line": ln, "text": text, "distinct": sorted(d), "shared": s}
                            for (ln, text), d, s in zip(clauses, distinct, shared)
                        ],
                    },
                    pre_priority=E7_BASE_PRIORITY
                    + E7_ZERO_WEIGHT * min(len(zero), E7_ZERO_CAP)
                    + E7_SHARED_WEIGHT,
                )
            )  # fmt: skip
    return out


def attach_e7(cands: list[Candidate], ctx: Ctx) -> None:
    """DESIGN 4.8 `attach`: the clause-by-text grid, one entry per clause (at most 5); `priority = pre_priority`."""
    for c in cands:
        f = c.features
        rows = f["clauses"]
        keep = [f["best"], *f["zero"][:E7_ZERO_CAP]]
        keep += [k for k in range(len(rows)) if k not in keep]
        c.evidence = [
            _ev(
                "plan",
                rows[k]["line"],
                f"clause {k + 1}: '{rows[k]['text'][:E7_CLAUSE_TEXT_MAX]}' - tokens found in the block: "
                + (", ".join(rows[k]["shared"]) or "none"),
            )
            for k in sorted(keep[:EVIDENCE_MAX])
        ]
        c.priority = c.pre_priority


EXTRACTORS["E7"] = (find_e7, attach_e7)


# ---------------------------------------------------------------- E6 (class C3, experimental): read and never written
#
# DESIGN 4.7. Lexical only: `find_e6` keeps the read quotes in `features`; `attach_e6` writes the evidence. Every item
# carries `features["experimental"] = True` (the lowest-trust extractor; the item JSON and the sheet label come from it).

E6_BASE_PRIORITY, E6_PER_READ, E6_READ_CAP = 20, 5, 3
E6_LITERAL_MAX = 80
# words are looked for in the prose of a sentence (backticked spans blanked out); the signs in the whole sentence
_E6_READ_WORD = re.compile(
    r"(?<![\w-])(?:keys on|when|is read|returns for|depends on)(?![\w-])", re.I
)
_E6_WRITE_WORD = re.compile(
    r"(?<![\w-])(?:sets|gives|writes|assigns|produces|returns(?! for(?![\w-])))(?![\w-])",
    re.I,
)
_E6_READ_SIGN = re.compile(r"==")
_E6_WRITE_SIGN = re.compile(r"(?<![=!<>])=(?![=>])")


def _e6_position(flat: str, word: re.Pattern, sign: re.Pattern) -> bool:
    prose = _E5_TICKED.sub(lambda m: " " * len(m.group(0)), flat)
    return word.search(prose) is not None or sign.search(flat) is not None


def _e6_literal_ok(span: str) -> bool:
    """A backticked span that is a value: not a command (more than one word, the first one a command word of E2), not
    a path or a glob, 80 characters or fewer."""
    return (
        bool(span)
        and len(span) <= E6_LITERAL_MAX
        and not (" " in span and span.split(None, 1)[0] in E2_FIRST_WORDS)
        and re.fullmatch(formats.PATH_TOKEN, span) is None
    )


def _e6_has(sentence: str, literal: str) -> bool:
    """The literal occurs in the sentence (backticked or bare), not as part of a longer word."""
    pre = r"(?<![\w])" if literal[0].isalnum() or literal[0] == "_" else ""
    post = r"(?![\w])" if literal[-1].isalnum() or literal[-1] == "_" else ""
    return re.search(pre + re.escape(literal) + post, sentence) is not None


def _e6_sentences(doc: plan.Doc):
    """(plan line, last line, flattened sentence, first line of it) of every sentence of the task, criterion and
    constraint blocks. A bullet or a paragraph is read apart (a `Depends on:` line is not a sentence)."""
    for b in doc.of("task", "criterion", "constraint"):
        items: list[list] = []
        for n, raw in enumerate(b["text"].split("\n"), b["line_start"]):
            if not raw.strip():
                items.append([n, ""])
            elif items and items[-1][1] and not _E5_BULLET.match(raw):
                items[-1][1] += "\n" + raw
            else:
                items.append([n, _E5_BULLET.sub("", raw, count=1)])
        for first, text in items:
            if _E5_DEPENDS.match(text):
                continue
            for start, _, sent in plan.sentences(text):
                line = first + text.count("\n", 0, start)
                yield (
                    line,
                    line + sent.count("\n"),
                    b["task"],
                    fnd.flat(sent),
                    fnd.flat(sent.split("\n")[0]),
                )


# Where I narrowed or interpreted DESIGN 4.7 (each is also in the Task 18 report):
#  1. "Anywhere in the candidate" is the three input blocks (task, criterion, constraint), which together hold every
#     line of the plan body except titles and front matter; a write sentence in a heading is not seen.
#  2. A read or write WORD is looked for in the sentence with its backticked spans blanked out (a word inside a span,
#     such as `sets`, is a value and not a position); the SIGNS "==" and "=" are looked for in the whole sentence,
#     because they live inside code spans (`legal_hold = false` is a write of legal_hold). "=" is a write only when it
#     stands alone (not "==", "!=", "<=", ">=", "=>"). "keys on", "is read", "returns for" and "depends on" are exact
#     phrases; no other inflection is read.
#  3. A "literal" is a backticked span of 80 characters or fewer that is not a command (more than one word, the first
#     one a command word of E2: grep, egrep, rg, git, pytest, test) and not a path or glob token (E4 makes a similar
#     cut), compared exactly (case-sensitive, trimmed).
#  4. A write occurrence is the literal anywhere in a write sentence, backticked or bare, as a whole word; so
#     "sets legal_hold" without backticks also clears it, and a sentence that both reads and writes it clears it.
#  5. Each read sentence counts once per literal (read_count); the candidate sits on the first read sentence, whose
#     first 200 characters (or its first line, when the wrapped sentence is not a quote of the plan) are the anchor.
#  6. The evidence is up to 3 read quotes (the cap of read_count) and the zero line, not the single quote.
def find_e6(doc: plan.Doc, ctx: Ctx) -> list[Candidate]:
    """DESIGN 4.7 `find`: one candidate per literal that is read at least once and written nowhere."""
    sents = list(_e6_sentences(doc))
    written = [
        flat
        for _, _, _, flat, _ in sents
        if _e6_position(flat, _E6_WRITE_WORD, _E6_WRITE_SIGN)
    ]
    reads: dict[str, list[tuple]] = {}
    for line, end, task, flat, first in sents:
        if not _e6_position(flat, _E6_READ_WORD, _E6_READ_SIGN):
            continue
        for lit in dict.fromkeys(m.group(1).strip() for m in _E5_TICKED.finditer(flat)):
            if _e6_literal_ok(lit):
                reads.setdefault(lit, []).append((line, end, task, flat, first))
    out: list[Candidate] = []
    for lit, occ in reads.items():
        if any(_e6_has(w, lit) for w in written):
            continue
        for line, end, task, flat, first in occ:
            anchor = next(
                (
                    a
                    for a in (flat[:ANCHOR_MAX].rstrip(), first[:ANCHOR_MAX].rstrip())
                    if len(a) >= ANCHOR_MIN and a in ctx.flat_text
                ),
                None,
            )
            if anchor:
                break
        else:
            continue
        n = min(len({o[0] for o in occ}), E6_READ_CAP)
        out.append(
            Candidate(
                "E6", "C3", "unwritten", anchor,
                {"task": task, "line_start": line, "line_end": end},
                features={
                    "literal": lit, "experimental": True,
                    "read_count": len({o[0] for o in occ}), "write_count": 0,
                    "reads": [{"line": o[0], "text": o[3][:EVIDENCE_TEXT_MAX]} for o in occ[:E6_READ_CAP]],
                },
                pre_priority=E6_BASE_PRIORITY + E6_PER_READ * n,
            )
        )  # fmt: skip
    return sorted(out, key=lambda c: (c.location["line_start"], c.features["literal"]))


def attach_e6(cands: list[Candidate], ctx: Ctx) -> None:
    """DESIGN 4.7 `attach`: the read quotes and `write-position occurrences of '<literal>': 0`; `priority = pre_priority`."""
    for c in cands:
        f = c.features
        c.evidence = [_ev("plan", r["line"], r["text"]) for r in f["reads"]] + [
            _ev(
                "plan",
                c.location["line_start"],
                f"write-position occurrences of '{f['literal']}': {f['write_count']}",
            )
        ]
        c.priority = c.pre_priority


EXTRACTORS["E6"] = (find_e6, attach_e6)
