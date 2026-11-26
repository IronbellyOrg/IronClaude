#!/usr/bin/env python3
"""Surgical-remediation helper for /sc:workflow (standard library only).

Subcommands (all but ``route`` take ``--root <checkout>``; failures print
``E-REMEDIATE-*`` (or the helper's ``E-ARCHIVE-*``) on stderr and exit 1):

  route      print the remediation route as JSON
  reserve    pick a new package id and create the empty leaf in to-do/
  prepare    private copy of the old plan + source under /tmp
  archive    move a superseded package to archive/ and mark its contract
  place      fill the reserved leaf with the repaired package (surgical route)
  restore    undo ``archive`` (package back to to-do/, contract as before)
  mark       the one writer of review_verdict/open_blockers/superseded_by/...
  release    remove the reserved leaf when it is empty or holds only place output

Every move uses ``rename_noreplace`` of the sibling sc-implement-protocol
skill (loaded by file path); contracts are edited as text, never as YAML.
"""

import argparse
import datetime
import difflib
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROUTES = ("none", "surgical", "regenerate")

ID_RE = re.compile(r"^TASK-WF-([a-z][A-Za-z0-9]{0,15})-(\d{8}-\d{6})(?:-[2-9])?$")
COUNT_KEYS = ("blocking", "label_high", "medium", "note")
HELPER_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "sc-implement-protocol"
    / "scripts"
    / "archive_workspace.py"
)
UNDO_NAME = "archive-undo.txt"
# files `place` writes (relative to the new package); release removes only these
PLACE_FILES = (
    "{id}.md",
    "source.md",
    "return-contract.yaml",
    "artifacts/plan.diff",
    "artifacts/prior-findings.md",
    "artifacts/old-plan.md",
    "artifacts/revision-log.md",
)


class RemediateError(Exception):
    def __init__(self, code, msg):
        super().__init__(msg)
        self.code, self.msg = code, msg


# --------------------------------------------------------------------- route
def route(blocking, label_high, medium, regenerated_already=False, forced=None):
    """Return (route, forced). Rows in order, first match wins."""
    for name, v in (
        ("blocking", blocking),
        ("label_high", label_high),
        ("medium", medium),
    ):
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise ValueError(f"{name} must be a non-negative integer, got {v!r}")
    if forced is not None and forced not in ROUTES:
        raise ValueError(f"forced must be one of {ROUTES}, got {forced!r}")
    if forced is not None:
        result = forced
    elif blocking == 0:
        result = "none"
    elif blocking <= 3 and label_high <= 5 and medium <= 9:
        result = "surgical"
    else:
        result = "regenerate"
    if result == "regenerate" and regenerated_already:
        result = "escalate"
    return result, forced is not None


def _count(text):
    try:
        v = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not an integer: {text!r}")
    if v < 0:
        raise argparse.ArgumentTypeError(f"negative count: {v}")
    return v


def _cmd_route(args):
    r, forced = route(
        args.blocking,
        args.label_high,
        args.medium,
        args.regenerated_already,
        args.forced,
    )
    print(json.dumps({"route": r, "forced": forced}))
    return 0


# ------------------------------------------------------------------- helpers
def _fail(code, msg):
    raise RemediateError(code, msg)


def _check_id(value, what):
    if not isinstance(value, str) or not ID_RE.match(value):
        _fail("E-REMEDIATE-ID", f"{what} is not a TASK-WF package id: {value!r}")
    return value


def _tasks(root):
    root = Path(os.path.realpath(root))
    if not os.path.lexists(root / ".git"):
        _fail("E-REMEDIATE-ROOT", f"{root} is not a checkout root (.git missing)")
    return root, root / ".dev" / "tasks"


def _real_dir(p):
    return os.path.isdir(p) and not os.path.islink(p)


def _check_tree(root, tasks):
    """Fail closed unless .dev, tasks, to-do and archive (those that exist) are real dirs."""
    for d in (root / ".dev", tasks, tasks / "to-do", tasks / "archive"):
        if os.path.islink(d) or (os.path.lexists(d) and not os.path.isdir(d)):
            _fail(
                "E-REMEDIATE-ROOT",
                f"{d} must be a real directory (no symlink); nothing moved",
            )


def _load_helper():
    if not HELPER_PATH.is_file():
        _fail(
            "E-REMEDIATE-HELPER",
            f"sibling helper missing, nothing moved: {HELPER_PATH}",
        )
    spec = importlib.util.spec_from_file_location(
        "archive_workspace_helper", HELPER_PATH
    )
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:  # fail closed on any load problem
        _fail("E-REMEDIATE-HELPER", f"cannot load {HELPER_PATH}: {exc}")
    if not hasattr(mod, "rename_noreplace"):
        _fail("E-REMEDIATE-HELPER", f"{HELPER_PATH} has no rename_noreplace")
    return mod


def _move(helper, src, dst):
    try:
        helper.rename_noreplace(str(src), str(dst))
    except RemediateError:
        raise
    except Exception as exc:
        code = getattr(exc, "code", "E-REMEDIATE-MOVE")
        _fail(code, getattr(exc, "msg", str(exc)))


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _write_atomic(path, text):
    tmp = f"{path}.tmp-{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def _write_new(path, data):
    """Exclusive create (never overwrites)."""
    binary = isinstance(data, bytes)
    try:
        f = open(
            path, "xb" if binary else "x", **({} if binary else {"encoding": "utf-8"})
        )
    except FileExistsError:
        raise  # not ours: never remove it
    try:
        with f:
            f.write(data)
    except BaseException:
        try:  # the file is ours (just created); do not leave a partial one
            os.unlink(path)
        except OSError:
            pass
        raise


def _parse_counts(text):
    try:
        obj = json.loads(text)
    except ValueError as exc:
        _fail("E-REMEDIATE-COUNTS", f"--finding-counts is not JSON: {exc}")
    if (
        not isinstance(obj, dict)
        or set(obj) != set(COUNT_KEYS)
        or any(
            isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in obj.values()
        )
    ):
        _fail(
            "E-REMEDIATE-COUNTS",
            f"--finding-counts needs exactly {COUNT_KEYS} as non-negative integers",
        )
    return "{" + ", ".join(f'"{k}": {obj[k]}' for k in COUNT_KEYS) + "}"


# ------------------------------------------------------ contract text edits
def _key_idx(lines, key):
    rx = re.compile(rf"^{re.escape(key)}:(\s|$)")
    return [i for i, ln in enumerate(lines) if rx.match(ln)]


def _block_end(lines, i):
    """Index after the block lines (indented or '- ') that follow top-level line i."""
    j = i + 1
    last = i
    while j < len(lines):
        ln = lines[j]
        if ln.strip() == "":
            j += 1
            continue
        if ln[0] in " \t" or ln.startswith("- "):
            last = j
            j += 1
            continue
        break
    return last + 1


def _ins(lines, ops, idx, line):
    lines.insert(idx, line)
    ops.append(["ins", idx, line])


def _rep(lines, ops, idx, new):
    ops.append(["rep", idx, new, lines[idx]])
    lines[idx] = new


def _del(lines, ops, idx):
    ops.append(["del", idx, lines[idx]])
    del lines[idx]


def _append_idx(lines):
    return len(lines) - 1 if lines and lines[-1] == "" else len(lines)


def _set_key(lines, ops, key, value):
    """Replace the line of an existing key (dropping its block), else append once."""
    hits = _key_idx(lines, key)
    if len(hits) > 1:
        _fail("E-REMEDIATE-CONTRACT", f"key {key} already appears {len(hits)} times")
    new = f"{key}: {value}"
    if hits:
        i = hits[0]
        for _ in range(_block_end(lines, i) - i - 1):
            _del(lines, ops, i + 1)
        _rep(lines, ops, i, new)
    else:
        _ins(lines, ops, _append_idx(lines), new)


def _add_unresolved(lines, ops, item):
    q = json.dumps(item)
    hits = _key_idx(lines, "unresolved")
    if len(hits) > 1:
        _fail("E-REMEDIATE-CONTRACT", "key unresolved appears more than once")
    if not hits:
        at = _append_idx(lines)
        _ins(lines, ops, at, "unresolved:")
        _ins(lines, ops, at + 1, f"  - {q}")
        return
    i = hits[0]
    rest = lines[i].split(":", 1)[1].strip()
    if rest in ("", "~", "null", "[]"):
        if rest:
            _rep(lines, ops, i, "unresolved:")
            end = i + 1
        else:
            end = _block_end(lines, i)
        indent = "  "
        for ln in lines[i + 1 : end]:
            m = re.match(r"^(\s*)- ", ln)
            if m:
                indent = m.group(1)
                break
        _ins(lines, ops, end, f"{indent}- {q}")
    elif rest.startswith("[") and rest.endswith("]"):
        _rep(lines, ops, i, lines[i][: lines[i].rindex("]")] + f", {q}]")
    else:
        _fail("E-REMEDIATE-CONTRACT", f"cannot edit unresolved value: {rest!r}")


def _undo_ops(lines, ops):
    """Reverse `ops` (recorded by the helpers above) on `lines`; raise on mismatch."""
    for op in reversed(ops):
        kind = op[0]
        if kind == "ins":
            _, idx, line = op
            if idx >= len(lines) or lines[idx] != line:
                _fail(
                    "E-REMEDIATE-RESTORE",
                    f"contract changed since archive (line {idx})",
                )
            del lines[idx]
        elif kind == "rep":
            _, idx, new, orig = op
            if idx >= len(lines) or lines[idx] != new:
                _fail(
                    "E-REMEDIATE-RESTORE",
                    f"contract changed since archive (line {idx})",
                )
            lines[idx] = orig
        elif kind == "del":
            _, idx, orig = op
            lines.insert(idx, orig)
        else:
            _fail("E-REMEDIATE-RESTORE", f"unknown undo op {kind!r}")


# ------------------------------------------------------------------- reserve
def reserve(root, old_id, now=None):
    _check_id(old_id, "--old-id")
    root, tasks = _tasks(root)
    if not _real_dir(tasks / "to-do" / old_id):
        _fail(
            "E-REMEDIATE-SOURCE", f"{tasks / 'to-do' / old_id} is not a real directory"
        )
    subject = ID_RE.match(old_id).group(1)
    stamp = now or datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y%m%d-%H%M%S"
    )
    base = f"TASK-WF-{subject}-{stamp}"
    _check_id(base, "computed id")
    todo = tasks / "to-do"
    for suffix in [""] + [f"-{n}" for n in range(2, 10)]:
        cand = base + suffix
        if any(os.path.lexists(tasks / d / cand) for d in ("to-do", "done", "archive")):
            continue
        try:
            os.mkdir(todo / cand)  # plain exclusive mkdir, never -p
        except FileExistsError:
            continue
        return cand
    _fail("E-PACKAGE-COLLISION", f"{base} and suffixes -2..-9 are all taken")


# ------------------------------------------------------------------- prepare
def prepare(root, old_id, new_id):
    _check_id(old_id, "--old-id")
    _check_id(new_id, "--new-id")
    root, tasks = _tasks(root)
    old = tasks / "to-do" / old_id
    if not _real_dir(tasks / "to-do" / new_id):
        _fail("E-REMEDIATE-LEAF", f"reserved leaf missing: {tasks / 'to-do' / new_id}")
    plan, source = old / f"{old_id}.md", old / "source.md"
    for f in (plan, source):
        if os.path.islink(f) or not f.is_file():
            _fail("E-REMEDIATE-SOURCE", f"{f} must be a regular file")
    text = plan.read_text(encoding="utf-8")
    m = re.match(r"^(---\n)(.*?)(\n---\n)", text, re.S)
    if not m or not re.search(r"^slug:.*$", m.group(2), re.M):
        _fail("E-REMEDIATE-SOURCE", "plan has no front-matter slug line")
    front = re.sub(r"^slug:.*$", f"slug: {new_id}", m.group(2), count=1, flags=re.M)
    new_text = m.group(1) + front + m.group(3) + text[m.end() :]
    tmp = tempfile.mkdtemp(
        prefix="sc-workflow-revise.", dir="/tmp"
    )  # mktemp -d semantics
    copy = Path(tmp) / new_id
    copy.mkdir()
    (copy / f"{new_id}.md").write_text(new_text, encoding="utf-8")
    (copy / "source.md").write_bytes(source.read_bytes())
    return {"tmp_dir": tmp, "copy_dir": str(copy), "old_plan_sha256": _sha(plan)}


# ------------------------------------------------------------------- archive
def _contract_edit(text, key_values, item=None):
    lines = text.split("\n")
    ops = []
    if item is not None:
        _add_unresolved(lines, ops, item)
    for k, v in key_values:
        _set_key(lines, ops, k, v)
    return "\n".join(lines), ops


def _has_superseded_warning(text):
    """True when an item of the top-level `unresolved` list starts with SUPERSEDED.

    A mention elsewhere (another item's prose, the `superseded_by` key) is not a
    warning about this package. Reads the same list shapes `_add_unresolved` edits.
    """
    lines = text.split("\n")
    hits = _key_idx(lines, "unresolved")
    if not hits:
        return False
    i = hits[0]
    rest = lines[i].split(":", 1)[1].strip()
    if rest.startswith("["):
        # quote-aware: a comma inside one quoted item does not start a new item
        inner = rest[1 : rest.rfind("]")] if "]" in rest else rest[1:]
        items = re.findall(
            r"""\s*("(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^,"']+)\s*(?:,|$)""", inner
        )
    else:
        items = []
        for ln in lines[i + 1 : _block_end(lines, i)]:
            m = re.match(r"^\s*-\s+(.*)$", ln)
            if m:
                items.append(m.group(1))
    return any(
        re.match(r"superseded\b", it.strip().lstrip("\"'"), re.I) for it in items
    )


def archive(root, package, superseded_by):
    root, tasks = _tasks(root)
    _check_tree(root, tasks)
    pkg = Path(os.path.abspath(package))
    old_id = _check_id(pkg.name, "package")
    if os.path.realpath(pkg.parent) != str(tasks / "to-do"):
        _fail("E-REMEDIATE-SOURCE", f"{pkg} is not a direct child of to-do/ in {root}")
    if superseded_by != "none":
        _check_id(superseded_by, "--superseded-by")
    src, dst = tasks / "to-do" / old_id, tasks / "archive" / old_id
    if not _real_dir(src):
        _fail("E-REMEDIATE-SOURCE", f"{src} is not a real directory")
    if os.path.lexists(dst):
        _fail(
            "E-REMEDIATE-CONFLICT",
            f"archive destination exists: {dst}; nothing changed",
        )
    helper = _load_helper()
    contract = src / "return-contract.yaml"
    undo_ops = []
    created = not os.path.lexists(contract)
    if created:
        text = (
            'contract_version: "1.1"\nstatus: partial\n'
            f"slug: {old_id}\nplan_path: ./{old_id}.md\nsource_path: ./source.md\n"
        )
    else:
        if os.path.islink(contract) or not contract.is_file():
            _fail("E-REMEDIATE-CONTRACT", f"{contract} must be a regular file")
        text = contract.read_text(encoding="utf-8")
    had_marker = _has_superseded_warning(text)
    item = None
    if not had_marker:
        item = (
            f"SUPERSEDED by {superseded_by}: do not run /sc:implement on this package."
            if superseded_by != "none"
            else "SUPERSEDED: replaced by a newer package; the replacement id is unrecorded."
        )
    kvs = [("superseded_by", superseded_by)] if superseded_by != "none" else []
    new_text, undo_ops = _contract_edit(text, kvs, item)
    made_artifacts = not os.path.lexists(src / "artifacts")
    if not made_artifacts and not _real_dir(src / "artifacts"):
        _fail("E-REMEDIATE-SOURCE", "artifacts must be a real directory")
    if os.path.lexists(src / "artifacts" / UNDO_NAME):
        _fail(
            "E-REMEDIATE-CONFLICT",
            f"{src / 'artifacts' / UNDO_NAME} already exists; nothing moved, nothing deleted",
        )
    os.makedirs(dst.parent, exist_ok=True)
    _move(helper, src, dst)  # first mutation; fails closed with nothing moved
    try:
        if made_artifacts:
            os.mkdir(dst / "artifacts")
        record = {
            "created_contract": created,
            "made_artifacts": made_artifacts,
            "ops": undo_ops,
        }
        _write_new(dst / "artifacts" / UNDO_NAME, json.dumps(record) + "\n")
        _write_atomic(dst / "return-contract.yaml", new_text)
    except Exception as exc:
        try:  # best effort: put the package back untouched
            if made_artifacts and os.path.lexists(dst / "artifacts"):
                for n in os.listdir(dst / "artifacts"):
                    os.unlink(dst / "artifacts" / n)
                os.rmdir(dst / "artifacts")
            # absent before the move (checked above), so any such file is ours
            elif os.path.lexists(dst / "artifacts" / UNDO_NAME):
                os.unlink(dst / "artifacts" / UNDO_NAME)
            if created and os.path.lexists(dst / "return-contract.yaml"):
                os.unlink(dst / "return-contract.yaml")
            _move(helper, dst, src)
        except Exception as back:
            _fail(
                "E-REMEDIATE-ARCHIVE",
                f"{exc}; rollback failed ({back}); package is at {dst}",
            )
        _fail("E-REMEDIATE-ARCHIVE", f"{exc}; rolled back, package is in to-do/")
    return {
        "status": "archived",
        "path": str(dst),
        "added_unresolved": item is not None,
    }


def restore(root, old_id):
    _check_id(old_id, "--old-id")
    root, tasks = _tasks(root)
    _check_tree(root, tasks)
    src, dst = tasks / "archive" / old_id, tasks / "to-do" / old_id
    if not _real_dir(src):
        _fail("E-REMEDIATE-SOURCE", f"{src} is not a real directory")
    if os.path.lexists(dst):
        _fail("E-REMEDIATE-CONFLICT", f"{dst} exists; nothing changed")
    undo = src / "artifacts" / UNDO_NAME
    if not undo.is_file():
        _fail("E-REMEDIATE-RESTORE", f"{undo} missing; cannot undo archive")
    try:
        rec = json.loads(undo.read_text(encoding="utf-8"))
    except ValueError as exc:
        _fail("E-REMEDIATE-RESTORE", f"{undo} unreadable: {exc}")
    contract = src / "return-contract.yaml"
    restored = None
    if not rec["created_contract"]:
        lines = contract.read_text(encoding="utf-8").split("\n")
        _undo_ops(lines, rec["ops"])
        restored = "\n".join(lines)
    helper = _load_helper()
    _move(helper, src, dst)
    pkg = dst
    try:
        if rec["created_contract"]:
            os.unlink(pkg / "return-contract.yaml")
        else:
            _write_atomic(pkg / "return-contract.yaml", restored)
        os.unlink(pkg / "artifacts" / UNDO_NAME)
        if rec["made_artifacts"]:
            os.rmdir(pkg / "artifacts")
    except OSError as exc:
        _fail("E-REMEDIATE-RESTORE", f"moved back to {pkg} but cleanup failed: {exc}")
    return {"status": "restored", "path": str(pkg)}


# ---------------------------------------------------------------------- mark
def mark(
    package,
    review_fail=False,
    open_blockers=None,
    superseded_by=None,
    fix_cycles=None,
    supersedes=None,
    route_name=None,
    finding_counts=None,
):
    pkg = Path(package)
    contract = pkg / "return-contract.yaml"
    missing = not os.path.lexists(contract)
    if missing:
        if not _real_dir(pkg):
            _fail("E-REMEDIATE-CONTRACT", f"{pkg} is not a real package directory")
    elif os.path.islink(contract) or not contract.is_file():
        _fail("E-REMEDIATE-CONTRACT", f"{contract} must be a regular file")
    kvs = []
    if review_fail:
        ids = [x.strip() for x in (open_blockers or "").split(",") if x.strip()]
        if not ids:
            _fail("E-REMEDIATE-ARGS", "--review-fail needs --open-blockers <ids>")
        kvs.append(("review_verdict", "FAIL"))
        kvs.append(("open_blockers", json.dumps(ids)))
    elif open_blockers is not None:
        _fail("E-REMEDIATE-ARGS", "--open-blockers needs --review-fail")
    if superseded_by is not None:
        kvs.append(("superseded_by", _check_id(superseded_by, "--superseded-by")))
    if fix_cycles is not None:
        kvs.append(("fix_cycles", str(fix_cycles)))
    if supersedes is not None or route_name is not None or finding_counts is not None:
        if supersedes is None or route_name != "regenerate" or finding_counts is None:
            _fail(
                "E-REMEDIATE-ARGS",
                "--supersedes, --route regenerate and --finding-counts go together",
            )
        kvs.append(("supersedes", _check_id(supersedes, "--supersedes")))
        kvs.append(("remediation_route", route_name))
        kvs.append(("finding_counts", _parse_counts(finding_counts)))
    if not kvs:
        _fail("E-REMEDIATE-ARGS", "mark has nothing to write")
    # no contract yet (regenerate route, before Wave 5): minimal text, Wave 5 merges into it
    base = (
        f'contract_version: "1.1"\nstatus: partial\nslug: {pkg.resolve().name}\n'
        if missing
        else contract.read_text(encoding="utf-8")
    )
    new_text, _ = _contract_edit(base, kvs)
    _write_atomic(contract, new_text)
    return {"status": "marked", "keys": [k for k, _ in kvs]}


# --------------------------------------------------------------------- place
def _diff_w(old_text, new_text):
    a, b = old_text.splitlines(), new_text.splitlines()
    na, nb = ["".join(x.split()) for x in a], ["".join(x.split()) for x in b]
    sm = difflib.SequenceMatcher(None, na, nb, autojunk=False)
    out = ["--- old-plan", "+++ new-plan"]
    for group in sm.get_grouped_opcodes(3):
        i1, i2, j1, j2 = group[0][1], group[-1][2], group[0][3], group[-1][4]
        out.append(f"@@ -{i1 + 1},{i2 - i1} +{j1 + 1},{j2 - j1} @@")
        for tag, a1, a2, b1, b2 in group:
            if tag == "equal":
                out += [" " + x for x in a[a1:a2]]
            else:
                out += ["-" + x for x in a[a1:a2]] + ["+" + x for x in b[b1:b2]]
    return "\n".join(out) + ("\n" if len(out) > 2 else "")


def place(root, old_id, new_id, copy_dir, finding_counts, review):
    _check_id(old_id, "--old-id")
    _check_id(new_id, "--new-id")
    counts = _parse_counts(finding_counts)
    root, tasks = _tasks(root)
    leaf, old = tasks / "to-do" / new_id, tasks / "archive" / old_id
    if not _real_dir(leaf):
        _fail("E-REMEDIATE-LEAF", f"reserved leaf missing: {leaf}")
    if os.listdir(leaf):
        _fail("E-REMEDIATE-LEAF", f"reserved leaf is not empty: {leaf}")
    if os.path.lexists(tasks / "to-do" / old_id) or not _real_dir(old):
        _fail("E-REMEDIATE-SOURCE", f"{old_id} must be archived before place")
    copy, rev = Path(copy_dir), Path(review)
    if not os.path.lexists(rev):
        # a report inside the old package was moved by archive: use its archived path
        base = (tasks / "to-do" / old_id).parts
        parts = Path(os.path.realpath(rev)).parts
        if len(parts) > len(base) and parts[: len(base)] == base:
            rev = old.joinpath(*parts[len(base) :])
    new_plan, new_source = copy / f"{new_id}.md", copy / "source.md"
    old_plan, old_source = old / f"{old_id}.md", old / "source.md"
    for f in (new_plan, new_source, old_plan, old_source, rev):
        if os.path.islink(f) or not f.is_file():
            _fail("E-REMEDIATE-SOURCE", f"{f} must be a regular file")
    new_text = new_plan.read_text(encoding="utf-8")
    if not re.search(rf"^slug: {re.escape(new_id)}\s*$", new_text, re.M):
        _fail("E-REMEDIATE-SOURCE", f"{new_plan} slug is not {new_id}")
    old_text = old_plan.read_text(encoding="utf-8")
    src_text = old_source.read_text(encoding="utf-8")
    n = len(re.findall(r"^## Revision \d+", src_text, re.M)) + 1
    fixmap = copy / "fixmap.md"
    fix_text = fixmap.read_text(encoding="utf-8") if fixmap.is_file() else ""

    _write_new(leaf / f"{new_id}.md", new_text)
    revision = (
        ("" if src_text.endswith("\n") else "\n") + f"\n## Revision {n}\n\n"
        f"- Replaces package: {old_id} (archived under .dev/tasks/archive/{old_id}/)\n"
        f"- Review report: {rev}\n"
        "- Fix map: ./artifacts/revision-log.md (diff: ./artifacts/plan.diff)\n"
    )
    _write_new(leaf / "source.md", src_text + revision)
    (leaf / "artifacts").mkdir()
    _write_new(leaf / "artifacts" / "plan.diff", _diff_w(old_text, new_text))
    _write_new(leaf / "artifacts" / "prior-findings.md", rev.read_bytes())
    _write_new(leaf / "artifacts" / "old-plan.md", old_plan.read_bytes())
    log = (
        f"# Revision {n} log\n\n- old package: {old_id}\n- new package: {new_id}\n"
        f"- old plan sha256: {_sha(old_plan)}\n- review report: {rev}\n"
        f"- finding_counts: {counts}\n"
    )
    if fix_text:
        log += "\n## Fix map\n\n" + fix_text + ("" if fix_text.endswith("\n") else "\n")
    _write_new(leaf / "artifacts" / "revision-log.md", log)
    _write_new(
        leaf / "return-contract.yaml",
        'contract_version: "1.1"\n'
        f"supersedes: {old_id}\nremediation_route: surgical\nfinding_counts: {counts}\n",
    )
    return {"status": "placed", "path": str(leaf)}


def release(root, new_id):
    _check_id(new_id, "--new-id")
    root, tasks = _tasks(root)
    leaf = tasks / "to-do" / new_id
    if not os.path.lexists(leaf):
        return {"status": "absent"}
    if not _real_dir(leaf):
        _fail("E-REMEDIATE-RELEASE", f"{leaf} is not a real directory")
    allowed = {f.format(id=new_id) for f in PLACE_FILES}
    files, dirs = [], []
    for dp, dn, fn in os.walk(leaf, followlinks=False):
        rel = Path(dp).relative_to(leaf)
        for d in dn:
            r = str(rel / d)
            if r != "artifacts" or os.path.islink(Path(dp) / d):
                _fail(
                    "E-REMEDIATE-RELEASE",
                    f"{leaf / r} was not written by place; left alone",
                )
            dirs.append(Path(dp) / d)
        for f in fn:
            if str(rel / f) not in allowed:
                _fail(
                    "E-REMEDIATE-RELEASE",
                    f"{Path(dp) / f} was not written by place; left alone",
                )
            files.append(Path(dp) / f)
    for f in files:
        os.unlink(f)
    for d in dirs:
        os.rmdir(d)
    os.rmdir(leaf)
    return {"status": "released", "path": str(leaf)}


# ----------------------------------------------------------------------- CLI
def _cmd_reserve(a):
    print(reserve(a.root, a.old_id))
    return 0


def _json(fn):
    def run(a):
        print(json.dumps(fn(a)))
        return 0

    return run


def main(argv=None):
    p = argparse.ArgumentParser(prog="remediate.py")
    sub = p.add_subparsers(dest="command", required=True)

    def add(name, fn, root=True):
        s = sub.add_parser(name)
        if root:
            s.add_argument("--root", default=".", help="checkout root (default: cwd)")
        s.set_defaults(func=fn)
        return s

    r = add("route", _cmd_route, root=False)
    r.add_argument("--blocking", type=_count, required=True)
    r.add_argument("--label-high", type=_count, required=True)
    r.add_argument("--medium", type=_count, required=True)
    r.add_argument("--regenerated-already", action="store_true")
    r.add_argument("--forced", choices=ROUTES, default=None)

    s = add("reserve", _cmd_reserve)
    s.add_argument("--old-id", required=True)

    s = add("prepare", _json(lambda a: prepare(a.root, a.old_id, a.new_id)))
    s.add_argument("--old-id", required=True)
    s.add_argument("--new-id", required=True)

    s = add("archive", _json(lambda a: archive(a.root, a.package, a.superseded_by)))
    s.add_argument("--package", required=True)
    s.add_argument("--superseded-by", required=True, help="<new-id> or none")

    s = add(
        "place",
        _json(
            lambda a: place(
                a.root, a.old_id, a.new_id, a.copy_dir, a.finding_counts, a.review
            )
        ),
    )
    s.add_argument("--old-id", required=True)
    s.add_argument("--new-id", required=True)
    s.add_argument("--copy-dir", required=True)
    s.add_argument("--finding-counts", required=True)
    s.add_argument("--review", required=True)

    s = add("restore", _json(lambda a: restore(a.root, a.old_id)))
    s.add_argument("--old-id", required=True)

    s = add(
        "mark",
        _json(
            lambda a: mark(
                a.package,
                a.review_fail,
                a.open_blockers,
                a.superseded_by,
                a.fix_cycles,
                a.supersedes,
                a.route,
                a.finding_counts,
            )
        ),
        root=False,
    )
    s.add_argument("--package", required=True)
    s.add_argument("--review-fail", action="store_true")
    s.add_argument("--open-blockers")
    s.add_argument("--superseded-by")
    s.add_argument("--fix-cycles", type=_count)
    s.add_argument("--supersedes")
    s.add_argument("--route", choices=("regenerate",))
    s.add_argument("--finding-counts")

    s = add("release", _json(lambda a: release(a.root, a.new_id)))
    s.add_argument("--new-id", required=True)

    args = p.parse_args(argv)
    try:
        return args.func(args)
    except RemediateError as exc:
        print(f"{exc.code}: {exc.msg}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"E-REMEDIATE-IO: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
