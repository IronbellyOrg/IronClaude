"""Read-only inventory of the tests that pin the pr-submit protocol text (plan task 1, O3).

Prints, to stdout, every exact-text pin and every absence or line rule that a test
holds on the pr-submit skill folder or the pr-submit command file. Standard library
only; reads files, writes nothing, makes no network call. Run from the repo root:

    uv run python <this file>

A READER is a test function or helper that reads target text: it calls a read function
(read_text, _read, _prose, ...) on something that names a target file (a target token or
a module constant that, directly or through other constants, holds one), or loops over
such constants and reads the loop variable, or calls a helper that does. Tests that scan
whole folders through a constant that holds no target token are listed in FORCED_READERS
with the reason.

Pass A: every string literal of 8 or more characters, held by a reader or by a module
constant a reader uses, that appears verbatim in a target file (raw text or prose form)
and is not just a path.
Pass B: every reader, with the source of each assert and each regular-expression call.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SKILL_REL = "src/superclaude/skills/sc-pr-submit-protocol"
COMMAND_REL = "src/superclaude/commands/pr-submit.md"
TOKENS = (
    "sc-pr-submit-protocol",
    "pr-submit.md",
    "state-machine.md",
    "loop-guard.md",
    "ci-poll.md",
    "review-retrigger.md",
)
EXTRA_TESTS = (
    "tests/skills/test_worker_contract.py",
    "tests/commands/test_impact_command.py",
    "tests/core/test_how_we_work_routing_table.py",
)
# Readers the token rule cannot see: the write-verb audit scans every file under the skills,
# commands and agents folders (AUDIT_ROOTS), which includes the pr-submit files.
FORCED_READERS = {
    "tests/skills/test_worker_contract.py": (
        "test_every_write_verb_hit_is_classified",
        "test_classification_table_has_no_stale_entries",
        "test_each_classification_has_one_category_and_a_reason",
        "_check_all_classified",
        "_scan_write_verbs",
    )
}
READ_CALLS = {"read_text", "_read", "_prose", "_text", "read_bytes"}
LITERAL_CAP = 200
SOURCE_CAP = 600
PATHLIKE = re.compile(
    r"^[\w./*\[\]-]+\.(md|sh|py|yaml|yml|json|jsonl|toml)$|^(src|tests|docs|\.dev)/[\w./*-]*$"
)


def targets() -> dict[str, tuple[str, str]]:
    found = {}
    files = [REPO / COMMAND_REL] + sorted(
        p for p in (REPO / SKILL_REL).rglob("*") if p.is_file() and p.suffix in (".md", ".sh")
    )
    for path in files:
        raw = path.read_text(encoding="utf-8")
        prose = " ".join(raw.replace("\n> ", " ").split())
        found[str(path.relative_to(REPO))] = (raw, prose)
    return found


def scanned_tests() -> list[Path]:
    chosen = set((REPO / "tests/pr_submit").glob("*.py"))
    chosen.update(REPO / rel for rel in EXTRA_TESTS)
    for path in (REPO / "tests").rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "sc-pr-submit-protocol" in text or "pr-submit" in text:
            chosen.add(path)
    return sorted(p for p in chosen if p.exists())


def segment(source: str, node: ast.AST) -> str:
    return ast.get_source_segment(source, node) or ""


def short(text: str, cap: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= cap else text[:cap] + f" [+{len(text) - cap} chars]"


class Analysis:
    """Readers and the module constants they use, for one test file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.source = path.read_text(encoding="utf-8", errors="replace")
        self.tree = ast.parse(self.source)
        self.values: dict[str, ast.AST] = {}
        self.funcs: dict[str, ast.AST] = {}
        for node in self.tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.funcs[node.name] = node
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.values[target.id] = node.value
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value:
                self.values[node.target.id] = node.value
        self.target_names = self._target_names()
        rel = str(path.relative_to(REPO))
        forced = set(FORCED_READERS.get(rel, ()))
        self.readers = {n for n, fn in self.funcs.items() if n in forced or self._reads_target(fn, 0)}
        self.used_constants = self._used_constants()

    def _target_names(self) -> set[str]:
        hit = {n for n, v in self.values.items() if any(t in segment(self.source, v) for t in TOKENS)}
        changed = True
        while changed:
            changed = False
            for name, value in self.values.items():
                if name in hit:
                    continue
                if any(isinstance(s, ast.Name) and s.id in hit for s in ast.walk(value)):
                    hit.add(name)
                    changed = True
        return hit

    def _mentions(self, node: ast.AST, extra: set[str]) -> bool:
        if any(t in segment(self.source, node) for t in TOKENS):
            return True
        return any(isinstance(s, ast.Name) and (s.id in self.target_names or s.id in extra) for s in ast.walk(node))

    def _reads_target(self, fn: ast.AST, depth: int) -> bool:
        loop_vars: set[str] = set()
        # a parametrized test whose decorator names a target file reads through its parameters
        if any(self._mentions(d, set()) for d in getattr(fn, "decorator_list", [])):
            loop_vars.update(a.arg for a in fn.args.args)
        for sub in ast.walk(fn):
            if isinstance(sub, ast.For) and self._mentions(sub.iter, set()):
                loop_vars.update(n.id for n in ast.walk(sub.target) if isinstance(n, ast.Name))
        for sub in ast.walk(fn):
            if not isinstance(sub, ast.Call):
                continue
            func = sub.func
            if isinstance(func, ast.Attribute) and func.attr in READ_CALLS:
                if self._mentions(func.value, loop_vars):
                    return True
            elif isinstance(func, ast.Name) and func.id in READ_CALLS:
                if sub.args and self._mentions(sub.args[0], loop_vars):
                    return True
            elif isinstance(func, ast.Name) and func.id in self.funcs and depth < 3:
                if self._mentions(sub, loop_vars) or self._reads_target(self.funcs[func.id], depth + 1):
                    return True
        return False

    def _used_constants(self) -> set[str]:
        used: set[str] = set()
        frontier = [self.funcs[n] for n in self.readers]
        while frontier:
            node = frontier.pop()
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id in self.values and sub.id not in used:
                    used.add(sub.id)
                    frontier.append(self.values[sub.id])
        return used


def owner_map(tree: ast.Module) -> dict[int, tuple[str, str]]:
    """id(node) -> (base owner name, display label)."""
    out: dict[int, tuple[str, str]] = {}

    def mark(node: ast.AST, base: str, label: str) -> None:
        for sub in ast.walk(node):
            out[id(sub)] = (base, label)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            mark(node, node.name, node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None:
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            name = next((t.id for t in targets if isinstance(t, ast.Name)), "<module>")
            if isinstance(node.value, ast.Dict):
                for key, value in zip(node.value.keys, node.value.values):
                    label = f"{name}[{short(ast.unparse(key), 70)}]" if key is not None else name
                    mark(value, name, label)
            else:
                mark(node.value, name, name)
    return out


def how_checked(parents: dict[int, ast.AST], node: ast.AST) -> str:
    parent = parents.get(id(node))
    if isinstance(parent, ast.Compare):
        return "not in" if any(isinstance(op, ast.NotIn) for op in parent.ops) else (
            "in" if any(isinstance(op, ast.In) for op in parent.ops) else "compare"
        )
    if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Attribute):
        return f".{parent.func.attr}()"
    if isinstance(parent, (ast.Tuple, ast.List, ast.Set, ast.Dict)):
        return "set member"
    return "other"


def pass_a(analyses: list[Analysis], found: dict[str, tuple[str, str]]) -> list[str]:
    rows = []
    for an in analyses:
        owners = owner_map(an.tree)
        parents = {id(c): n for n in ast.walk(an.tree) for c in ast.iter_child_nodes(n)}
        seen = set()
        for node in ast.walk(an.tree):
            if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
                continue
            base, label = owners.get(id(node), ("<module>", "<module>"))
            if base not in an.readers and base not in an.used_constants:
                continue
            text = node.value
            if len(text) < 8 or PATHLIKE.match(text.strip()):
                continue
            hit_files = [rel for rel, (raw, prose) in found.items() if text in raw or text in prose]
            if not hit_files:
                continue
            row = (
                f"{an.path.relative_to(REPO)}::{label} | {', '.join(hit_files)} | "
                f"{how_checked(parents, node)} | {short(text.replace(chr(10), chr(92) + 'n'), LITERAL_CAP)}"
            )
            if row not in seen:
                seen.add(row)
                rows.append(row)
    return rows


def pass_b(analyses: list[Analysis]) -> list[str]:
    rows = []
    for an in analyses:
        for name in sorted(an.readers):
            fn = an.funcs[name]
            rows.append(f"{an.path.relative_to(REPO)}::{name}")
            for sub in ast.walk(fn):
                if isinstance(sub, ast.Assert):
                    rows.append("    assert: " + short(segment(an.source, sub), SOURCE_CAP))
                elif (
                    isinstance(sub, ast.Call)
                    and isinstance(sub.func, ast.Attribute)
                    and isinstance(sub.func.value, ast.Name)
                    and sub.func.value.id == "re"
                    and sub.func.attr in {"compile", "search", "match", "findall", "sub", "fullmatch"}
                ):
                    rows.append("    regex: " + short(segment(an.source, sub), SOURCE_CAP))
    return rows


def main() -> int:
    found = targets()
    analyses = [Analysis(p) for p in scanned_tests()]
    a_rows = pass_a(analyses, found)
    b_rows = pass_b(analyses)
    readers = sum(len(an.readers) for an in analyses)
    print("## Pass A: exact-text pins (test::owner | target file | how checked | literal)")
    print("\n".join(a_rows))
    print()
    print("## Pass B: readers of target text (test or helper), with their asserts and regex calls")
    print("\n".join(b_rows))
    print()
    print("## Footer")
    print("scanned test files:")
    print("\n".join(f"  {an.path.relative_to(REPO)}" for an in analyses))
    print("target files:")
    print("\n".join(f"  {rel}" for rel in found))
    print(f"pass A rows: {len(a_rows)}")
    print(f"pass B readers: {readers}")
    here = Path(__file__).resolve().relative_to(REPO)
    print(f"command: uv run python -I {here}")
    print(
        f"caps: literal display {LITERAL_CAP} characters, assert and regex source {SOURCE_CAP} "
        "characters; the full text is in the named test"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
