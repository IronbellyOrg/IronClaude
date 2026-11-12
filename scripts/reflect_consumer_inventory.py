#!/usr/bin/env python3
"""Consumer inventory of the reflect return-contract fields (contract compatibility gate, item 1).

Run with ``uv run python scripts/reflect_consumer_inventory.py [--out <file>] [--root <repo>]``. It reads files
only: no model, no process, no network. ``--root`` defaults to the repository that holds this script. ``--out``
defaults to ``<root>/.dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/consumer-inventory.md``
when that package folder exists, else ``./artifacts/consumer-inventory.md`` (relative to the working directory).

Words (WORDS): merge_method, adversarial_convergence_score, convergence_score, contract_version,
t2_model_class_diversity, t2_vendor_diversity, calibrator_diversity, reviewer_cards, citations_dropped. Each is
counted as a case-sensitive byte substring, occurrences per file (non-overlapping), so the convergence_score count
also includes every adversarial_convergence_score occurrence. The "lines" column counts the lines that hold at
least one word.

Scope (SCAN_ROOTS): src/, tests/, scripts/, .dev/eval-workspaces/ and docs/ under the root. The installed skill and
command primitives are scanned as part of src/ (src/superclaude/skills/ and src/superclaude/commands/); the report
gives their hit-file count separately. A missing scan root is listed as missing. Directories named in EXCLUDED_DIRS
(.git, __pycache__, node_modules, .venv, venv and tool caches) are not entered; symlinked directories are not
followed and are counted. The output file itself is skipped when it lies inside a scan root, so a rerun into the
same file reads the same tree.

Odd files never stop the run; each is counted and not searched: a file that cannot be stat'ed or read (unreadable,
for example a broken symlink), a path that is not a regular file (non-regular, for example a FIFO) and a file that
holds a NUL byte (binary).

Classification of each hit file (first match wins; ``rel`` is the path relative to the root, posix form). Every
hit file gets one of producer, validator, consumer or "not in scope", and a basis: ``named`` (rules 1-2, from a
list) or ``cue`` (rules 3-7, from the path or the text).
1. NAMED_ROLES, exact paths from the task's lists, the spec's "Deferred versioned change" list and the review fix:
   producer  - src/superclaude/skills/sc-reflect-protocol/SKILL.md (section 9.1 and Wave 5),
               src/superclaude/skills/sc-reflect-protocol/refs/report-template.md,
               src/superclaude/cli/reflect/ensemble.py (headless builder), and from the review fix
               refs/input-resolution.md (its table gives the t2_model_class_diversity values) and
               refs/reflection-rubric.md (it says calibrator_diversity is emitted into reflection-card.yaml);
   validator - src/superclaude/cli/reflect/contract.py (derive_verdict, _degraded_reason);
   consumer  - the section 9.3 map rows that have a file in this repository (sc-troubleshoot-protocol,
               sc-task-protocol, sc-tasklist-protocol and sc-workflow-protocol SKILL.md, task-builder SKILL.md with
               EV-4, refs/promotion-adapters.md for the Wave 7 adapters, the CI grader
               .dev/eval-workspaces/sc-reflect/grader.py, the sprint executor src/superclaude/cli/sprint/executor.py),
               refs/ops-integration.md (PromQL label list), and from the review fix the two files whose text opens
               return-contract.yaml and fails the gate on adversarial_convergence_score < 0.80:
               src/superclaude/skills/task/SKILL.md (the sc-task row) and
               src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md (the sc:tasklist row).
               sc-task-protocol/SKILL.md stays listed and shows "no match" when it names none of the words.
2. PREFIX_ROLES: tests/cli/reflect/ is consumer (deferred list item 9: fixtures and tests that carry merge_method).
3. A path with a component containing "roadmap" (any letter case) is "not in scope": the roadmap pipeline uses the
   same words for its own merge and contract.
4. Test cue: a directory component named tests, test or fixtures, or a file name test_*, *_test.py or conftest.py
   is consumer.
5. Write cue, producer, by file suffix (a "word" is one of WORDS, on the same line as the cue):
   .py   - a quoted word followed by ``:`` (dict key) or by ``] =`` (subscript assignment), or the bare word
           followed by ``=`` (assignment or keyword argument) or by ``: <type> =`` (annotated assignment), never ``==``;
   .json - a double-quoted word followed by ``:``;
   .yaml, .yml - a line that starts with the word as a key (optionally quoted, optionally after ``- ``) and ``:``
           followed by a space or the line end;
   .md   - the .yaml key form or the .json key form on a line inside a fenced code block (``` or ~~~).
6. Check cue, validator: a .py file with a line that holds a word and ``==``, ``!=``, ``<=``, ``>=``, `` < ``,
   `` > ``, ``assert`` or ``raise``.
7. Everything else is consumer.
For a cue-based row, ``consumer`` means "references the field; not proof it is read at runtime", and producer or
validator means the file text matched that cue, not that its code was traced. Named items with no file in the
repository (the meta-eval runs.jsonl aggregator and the sc:roadmap validation gate) are listed as UNVERIFIED;
Python files under the scan roots that name runs.jsonl are listed as aggregator candidates (the listing does not
change their role).

Negative statements: the report says whether any line under src/ holds a ``contract_version == "1.8.0"`` equality
(on one line: the name, up to 40 characters other than "=", ``==``, then 1.8.0 in single or double quotes; or the
quoted 1.8.0, ``==``, up to 40 characters, then the name; for example ``c.get("contract_version") == '1.8.0'``),
listing each hit with path, line and code (.py) or prose; and whether
.dev/eval-workspaces/sc-reflect/grader.py matches any word or ``convergence``, listing the counts when it does.

Determinism: sorted traversal, paths relative to the root, no timestamp; the same tree gives the same bytes.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
from pathlib import Path

WORDS = (
    "merge_method",
    "adversarial_convergence_score",
    "convergence_score",
    "contract_version",
    "t2_model_class_diversity",
    "t2_vendor_diversity",
    "calibrator_diversity",
    "reviewer_cards",
    "citations_dropped",
)
SCAN_ROOTS = ("src", "tests", "scripts", ".dev/eval-workspaces", "docs")
PRIMITIVE_PREFIXES = ("src/superclaude/skills/", "src/superclaude/commands/")
EXCLUDED_DIRS = frozenset(
    {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        ".tox",
        ".cache",
        ".hypothesis",
    }
)
PACKAGE = ".dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912"
GRADER = ".dev/eval-workspaces/sc-reflect/grader.py"
ROLE_ORDER = ("producer", "validator", "consumer", "not in scope")
BASES = ("named", "cue")

_SKILL = "src/superclaude/skills/sc-reflect-protocol"
NAMED_ROLES = {
    f"{_SKILL}/SKILL.md": (
        "producer",
        "section 9.1 and Wave 5 (it also reads the fields in EV-1 and the Wave 7 gate)",
    ),
    f"{_SKILL}/refs/report-template.md": (
        "producer",
        "REPORT.md skeleton of the fields",
    ),
    "src/superclaude/cli/reflect/ensemble.py": (
        "producer",
        "headless contract builder",
    ),
    "src/superclaude/cli/reflect/contract.py": (
        "validator",
        "derive_verdict, _degraded_reason",
    ),
    f"{_SKILL}/refs/input-resolution.md": (
        "producer",
        "review fix: its table gives the t2_model_class_diversity values",
    ),
    f"{_SKILL}/refs/reflection-rubric.md": (
        "producer",
        "review fix: says calibrator_diversity is emitted into reflection-card.yaml",
    ),
    "src/superclaude/skills/task/SKILL.md": (
        "consumer",
        "section 9.3 sc-task row (review fix): opens return-contract.yaml, "
        "fails the gate on adversarial_convergence_score < 0.80",
    ),
    "src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md": (
        "consumer",
        "section 9.3 sc:tasklist row (review fix): opens return-contract.yaml, "
        "fails the gate on adversarial_convergence_score < 0.80",
    ),
    f"{_SKILL}/refs/ops-integration.md": ("consumer", "PromQL label list"),
    f"{_SKILL}/refs/promotion-adapters.md": (
        "consumer",
        "section 9.3 Wave 7 promotion adapters",
    ),
    "src/superclaude/skills/task-builder/SKILL.md": (
        "consumer",
        "section 9.3 row, EV-4",
    ),
    "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md": (
        "consumer",
        "section 9.3 row",
    ),
    "src/superclaude/skills/sc-task-protocol/SKILL.md": (
        "consumer",
        "section 9.3 sc-task row as first mapped; the gate text is in skills/task/SKILL.md",
    ),
    "src/superclaude/skills/sc-tasklist-protocol/SKILL.md": (
        "consumer",
        "section 9.3 sc:tasklist gate",
    ),
    "src/superclaude/skills/sc-workflow-protocol/SKILL.md": (
        "consumer",
        "section 9.3 row, deferred item 10",
    ),
    "src/superclaude/cli/sprint/executor.py": (
        "consumer",
        "section 9.3 sprint executor, deferred item 8",
    ),
    GRADER: ("consumer", "section 9.3 CI grader"),
}
PREFIX_ROLES = (
    ("tests/cli/reflect/", "consumer", "deferred item 9 (reflect tests and fixtures)"),
)
UNVERIFIED_ITEMS = (
    (
        "meta-eval runs.jsonl aggregator (section 9.3, deferred item 7)",
        "no file in this repository is named as the aggregator; see the candidate list",
    ),
    (
        "sc:roadmap validation gate (section 9.3)",
        "no reflect-contract reader located; roadmap files are not in scope",
    ),
)
_EQUALITY = (
    re.compile(rb"contract_version[^\n=]{0,40}==\s*[\"']1\.8\.0[\"']"),
    re.compile(rb"[\"']1\.8\.0[\"']\s*==[^\n]{0,40}contract_version"),
)
_WORD_BYTES = tuple(w.encode() for w in WORDS)
_W = rb"(?:" + b"|".join(_WORD_BYTES) + rb")"
TEST_DIRS = frozenset({"tests", "test", "fixtures"})
_PY_WRITE = re.compile(
    rb"[\"']" + _W + rb"[\"']\s*(?::|\]\s*=(?!=))"
    rb"|\b" + _W + rb"\s*(?::[^=\n]*)?=(?!=)"
)
_JSON_KEY = re.compile(rb'"' + _W + rb'"\s*:')
_YAML_KEY = re.compile(rb"\s*(?:-\s+)?[\"']?" + _W + rb"[\"']?\s*:(?:\s|$)")
_PY_CHECK = re.compile(rb"==|!=|<=|>=|\s[<>]\s|\bassert\b|\braise\b")


def _writes(suffix: str, lines: list[bytes]) -> bool:
    """Rule 5 of the module docstring: does any line hold a write cue for this file suffix."""
    if suffix == "py":
        return any(_PY_WRITE.search(ln) for ln in lines)
    if suffix == "json":
        return any(_JSON_KEY.search(ln) for ln in lines)
    if suffix in ("yaml", "yml"):
        return any(_YAML_KEY.match(ln) for ln in lines)
    if suffix == "md":
        fenced = False
        for ln in lines:
            if ln.lstrip().startswith((b"```", b"~~~")):
                fenced = not fenced
            elif fenced and (_YAML_KEY.match(ln) or _JSON_KEY.search(ln)):
                return True
    return False


def classify(rel: str, data: bytes = b"") -> tuple[str, str, str]:
    """Return (role, basis, source) for a root-relative posix path and its bytes (rules 1-7 of the module docstring)."""
    if rel in NAMED_ROLES:
        return (NAMED_ROLES[rel][0], "named", NAMED_ROLES[rel][1])
    for prefix, role, source in PREFIX_ROLES:
        if rel.startswith(prefix):
            return role, "named", source
    parts = rel.split("/")
    if any("roadmap" in part.lower() for part in parts):
        return "not in scope", "cue", "roadmap pipeline (own merge and contract)"
    name = parts[-1]
    if (
        TEST_DIRS.intersection(parts[:-1])
        or name.startswith("test_")
        or name.endswith("_test.py")
        or name == "conftest.py"
    ):
        return "consumer", "cue", "test or test fixture"
    suffix = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    lines = data.split(b"\n")
    if _writes(suffix, lines):
        return "producer", "cue", "write cue"
    if suffix == "py" and any(
        _PY_CHECK.search(ln) for ln in lines if any(w in ln for w in _WORD_BYTES)
    ):
        return "validator", "cue", "check cue"
    return "consumer", "cue", "names a field"


def scan(root: Path, skip: Path | None = None) -> dict:
    """Walk the scan roots under root and return counts, hits and the two negative-statement checks."""
    res = {
        "missing_roots": [],
        "scanned": 0,
        "binary": [],
        "unreadable": [],
        "nonregular": [],
        "symlink_dirs": [],
        "hits": {},
        "equality": [],
        "runs_jsonl_py": [],
    }
    skip_resolved = skip.resolve() if skip is not None else None
    for top in SCAN_ROOTS:
        base = root / top
        if not base.is_dir():
            res["missing_roots"].append(top)
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            here = Path(dirpath)
            keep = []
            for d in sorted(dirnames):
                if d in EXCLUDED_DIRS:
                    continue
                if (here / d).is_symlink():
                    res["symlink_dirs"].append((here / d).relative_to(root).as_posix())
                    continue
                keep.append(d)
            dirnames[:] = keep
            for name in sorted(filenames):
                path = here / name
                rel = path.relative_to(root).as_posix()
                try:
                    if skip_resolved is not None and path.resolve() == skip_resolved:
                        continue
                    mode = os.stat(path).st_mode
                except (OSError, RuntimeError):
                    res["unreadable"].append(rel)
                    continue
                if not stat.S_ISREG(mode):
                    res["nonregular"].append(rel)
                    continue
                try:
                    data = path.read_bytes()
                except OSError:
                    res["unreadable"].append(rel)
                    continue
                if b"\0" in data:
                    res["binary"].append(rel)
                    continue
                res["scanned"] += 1
                _inspect(rel, data, res)
    return res


def _inspect(rel: str, data: bytes, res: dict) -> None:
    counts = [data.count(w) for w in _WORD_BYTES]
    lines = data.split(b"\n")
    if any(counts):
        hit_lines = sum(1 for ln in lines if any(w in ln for w in _WORD_BYTES))
        role, basis, _ = classify(rel, data)
        res["hits"][rel] = (counts, hit_lines, role, basis)
    if rel.endswith(".py") and b"runs.jsonl" in data:
        res["runs_jsonl_py"].append(rel)
    if rel.startswith("src/") and b"1.8.0" in data:
        for no, ln in enumerate(lines, 1):
            if any(p.search(ln) for p in _EQUALITY):
                kind = "code" if rel.endswith(".py") else "prose"
                res["equality"].append((rel, no, kind))


def _grader_line(root: Path, res: dict) -> str:
    path = root / GRADER
    if not path.is_file():
        return f"- `{GRADER}` was not found (UNVERIFIED)."
    try:
        data = path.read_bytes()
    except OSError:
        return f"- `{GRADER}` could not be read (UNVERIFIED)."
    found = [(w, data.count(w.encode())) for w in (*WORDS, "convergence")]
    found = [(w, n) for w, n in found if n]
    if not found:
        return (
            f"- `{GRADER}` has no match for any of the nine words or for `convergence`. "
            "It needs no change while the contract stays 1.8.0."
        )
    listed = ", ".join(f"`{w}` {n}" for w, n in found)
    return f"- CONTRADICTED: `{GRADER}` matches: {listed}."


def _equality_line(res: dict) -> list[str]:
    eq = res["equality"]
    if not eq:
        return [
            '- No `contract_version == "1.8.0"` equality exists in `src/` (either order, single or double quotes).',
        ]
    out = [
        f'- CONTRADICTED: {len(eq)} line(s) in `src/` hold a `contract_version == "1.8.0"` equality:'
    ]
    out += [f"  - `{rel}:{no}` ({kind})" for rel, no, kind in eq]
    code = sum(1 for _, _, kind in eq if kind == "code")
    out.append(f"  - Python code lines among them: {code}.")
    return out


def render(root: Path, res: dict) -> str:
    """Render the inventory as markdown (no timestamp, root-relative paths only)."""
    rows = []
    for rel, (counts, hit_lines, role, basis) in res["hits"].items():
        rows.append((ROLE_ORDER.index(role), rel, role, basis, counts, hit_lines))
    rows.sort(key=lambda r: (r[0], r[1]))
    by_role = {role: sum(1 for r in rows if r[2] == role) for role in ROLE_ORDER}
    by_basis = {basis: sum(1 for r in rows if r[3] == basis) for basis in BASES}
    primitives = sum(1 for r in rows if r[1].startswith(PRIMITIVE_PREFIXES))
    per_root = {
        top: sum(1 for r in rows if r[1].startswith(top + "/")) for top in SCAN_ROOTS
    }

    out = ["# Reflect return-contract consumer inventory", ""]
    out.append(
        "Generated by `uv run python scripts/reflect_consumer_inventory.py`. No timestamp; paths are relative"
    )
    out.append(
        "to the repository root. Rerun with `--out <file>` and diff to see what changed."
    )
    out += ["", "Words: " + ", ".join(f"`{w}`" for w in WORDS) + "."]
    out.append("Scan roots: " + ", ".join(f"`{t}/`" for t in SCAN_ROOTS) + ".")
    out += ["", "## Summary", ""]
    out.append(f"- Files searched: {res['scanned']}.")
    out.append(
        f"- Not searched: binary {len(res['binary'])}, unreadable {len(res['unreadable'])}, "
        f"non-regular {len(res['nonregular'])}, symlinked directories not followed {len(res['symlink_dirs'])}."
    )
    missing = ", ".join(f"`{m}/`" for m in res["missing_roots"]) or "none"
    out.append(f"- Missing scan roots: {missing}.")
    out.append(f"- Hit files: {len(rows)}.")
    out.append(
        "- Hit files by role: "
        + ", ".join(f"{role} {by_role[role]}" for role in ROLE_ORDER)
        + "."
    )
    out.append(
        "- Hit files by basis: "
        + ", ".join(f"{basis} {by_basis[basis]}" for basis in BASES)
        + "."
    )
    out.append(
        "- Hit files by scan root: "
        + ", ".join(f"`{t}/` {per_root[t]}" for t in SCAN_ROOTS)
        + "."
    )
    out.append(
        f"- Of the `src/` hit files, {primitives} are installed skill or command primitives "
        "(`src/superclaude/skills/`, `src/superclaude/commands/`)."
    )
    out += ["", "## Negative statements", ""]
    out += _equality_line(res)
    out.append(
        "- The Task 15 lint (`src/superclaude/cli/reflect/panel_lint.py`) checks the version as "
        '`version != CONTRACT_VERSION` with `CONTRACT_VERSION = "1.8.0"`, not as the literal equality this search '
        "looks for, so a rerun does not list it here."
    )
    out.append(_grader_line(root, res))

    out += ["", "## Named role files", ""]
    out.append("| File | Role | Source of the role | On disk | Hit |")
    out.append("|---|---|---|---|---|")
    named = [(p, r, s) for p, (r, s) in NAMED_ROLES.items()]
    named += [(p, r, s) for p, r, s in PREFIX_ROLES]
    for path, role, source in sorted(
        named, key=lambda n: (ROLE_ORDER.index(n[1]), n[0])
    ):
        on_disk = (root / path).exists()
        if path.endswith("/"):
            hit = sum(1 for r in rows if r[1].startswith(path))
            hit_text = f"{hit} file(s)"
        else:
            hit_text = "yes" if path in res["hits"] else "no match"
        disk_text = "yes" if on_disk else "no (UNVERIFIED)"
        out.append(f"| `{path}` | {role} | {source} | {disk_text} | {hit_text} |")
    out += [
        "",
        "UNVERIFIED (named consumers with no file located in this repository):",
        "",
    ]
    for item, why in UNVERIFIED_ITEMS:
        out.append(f"- {item}: {why}.")
    cands = ", ".join(f"`{p}`" for p in sorted(res["runs_jsonl_py"])) or "none"
    out.append(
        f"- Python files under the scan roots that name `runs.jsonl` (aggregator candidates): {cands}."
    )
    out.append(
        "- A named consumer marked `no match` exists but names none of the words; the code that reads the "
        "return contract there, if any, is UNVERIFIED."
    )

    out += ["", "## Hit files", ""]
    out.append(
        "Basis `named`: the role comes from the named lists. Basis `cue`: the role comes from the path or text cues"
    )
    out.append(
        "of the script docstring; a cue-based `consumer` references the field, which is not proof it is read at runtime."
    )
    out.append("")
    out.append(
        "| File | Role | Basis | Lines | " + " | ".join(f"`{w}`" for w in WORDS) + " |"
    )
    out.append("|---|---|---|---|" + "---|" * len(WORDS))
    for _, rel, role, basis, counts, hit_lines in rows:
        out.append(
            f"| `{rel}` | {role} | {basis} | {hit_lines} | "
            + " | ".join(str(c) for c in counts)
            + " |"
        )

    out += ["", "## Files not searched", ""]
    for label, key in (
        ("Binary", "binary"),
        ("Unreadable", "unreadable"),
        ("Non-regular", "nonregular"),
        ("Symlinked directories", "symlink_dirs"),
    ):
        items = ", ".join(f"`{p}`" for p in res[key]) or "none"
        out.append(f"- {label}: {items}.")

    out += ["", "## What this grep does and does not catch", ""]
    out += [
        "- It catches each word as a case-sensitive substring in any text file under the scan roots, prose,",
        "  fixtures and code alike. The `convergence_score` column includes the `adversarial_convergence_score`",
        "  occurrences.",
        "- It does not catch a field reached by a computed key (`'merge_' + 'method'`, f-strings), other spellings",
        "  (`convergence-score`, `mergeMethod`, the prose words 'convergence score'), a consumer that reads the",
        "  whole contract without naming the field, binary files, symlinked directories, or files outside the scan",
        "  roots (`plugins/`, `.claude/`, `~/.claude/`, `.dev/` outside `eval-workspaces/`, other repositories).",
        "- A `named` role says where a file sits in the named lists; a `cue` role says which path or text cue of",
        "  the script docstring the file matched. Neither comes from tracing the code, so neither proves that the",
        "  file writes or reads a field at runtime. The named list is not complete.",
        "",
    ]
    return "\n".join(out)


def default_out(root: Path) -> Path:
    package = root / PACKAGE
    if package.is_dir():
        return package / "artifacts" / "consumer-inventory.md"
    return Path("artifacts") / "consumer-inventory.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        print(f"root is not a directory: {args.root}", file=sys.stderr)
        return 2
    out = args.out if args.out is not None else default_out(root)
    res = scan(root, skip=out)
    text = render(root, res)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    rows = [hit[2] for hit in res["hits"].values()]
    roles = ", ".join(f"{role} {rows.count(role)}" for role in ROLE_ORDER)
    print(
        f"wrote {out}: {len(rows)} hit files ({roles}); searched {res['scanned']} files"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
