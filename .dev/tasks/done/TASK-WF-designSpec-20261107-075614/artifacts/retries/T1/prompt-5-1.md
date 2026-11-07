69f360d58d89456f559ad3de21ea75027cd72bb0
Review one task for spec compliance.

Task brief: ## Task 1: Write the pre-build record `./artifacts/pre-build-gate.md`

Create `./artifacts/pre-build-gate.md` in this package from ./source.md sections 6, 8 and 10. First record the base-commit state: run `make lint`, `uv run ruff format --check src/ tests/` and the full suite `uv run pytest -q tests` before any code edit and write each exit code, the pass count and every failing test id (or "clean") into the file, so later failures can be told apart from this feature's. Then record the release-gate decision of ./source.md section 8 in the owner's words: the build proceeds with no GitHub calls (fake `gh` in tests); gates G1 (live part), G2 (live part), G4, G5 and G6 are a release gate that the owner runs on a disposable fork PR before the feature is merged or turned on by default; the user guide states that draft behaviour is unverified until then; the PR body states the gate plainly; the run that opens the PR must pass `--merge-guard off`. Then close the open items by reading the code: O1, where `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (Wave 3 to Wave 6 and Wave 8 text) and `refs/loop-guard.md` assign a fix or CI cycle's `cycle_id` today and whether any test under `tests/pr_submit/` pins a value; O2, how scripts are granted and invoked in the SKILL front matter and what `test_allowed_tools_cover_every_program` in `tests/pr_submit/test_conflict_sync_protocol.py` and the `_RESOLUTION_SCRIPTS` tests in `tests/pr_submit/test_static_grep.py` require of a new script; O3, every exact-text pin and line-content rule (for example `test_intent_and_validator_lines_say_tier_2`, `test_skill_forbids_force_push`, the wait-only sentences pinned for `refs/state-machine.md`, and the `WRITE_VERB_CLASSIFICATION` table with its stale-entry test in `tests/skills/test_worker_contract.py`) on `SKILL.md`, `refs/state-machine.md`, `refs/loop-guard.md` and `src/superclaude/commands/pr-submit.md` that the later additive edits must avoid; O4, that the S5a re-trigger sentence in `SKILL.md` stays unchanged and where the new release sentence goes relative to it; and the literal start text of the S5a sentence and of the Wave 6 pre-push sentence as the existing pins write them, so later tests can compare against string constants.

Acceptance criteria:
- T1.AC1: `./artifacts/pre-build-gate.md` has the base-commit record (three commands, exit codes, the full-suite pass count and failing test ids, or "clean") and one row each for G1 to G6: G1 to G3 `CONFIRMED` for the locally verifiable part with the evidence named in ./source.md, G1 and G2 live parts, G4, G5 and G6 `OPEN` as a release gate with the owner decision quoted.
- T1.AC2: O1 to O4 each carry the finding with the file and symbol read in this task (no bare line numbers); O1 names one single place where the guard-enabled cycle id is minted so the push triad and `rereview_requested` use the same id, or states that no id is minted today and which sentence will mint it.
- T1.AC3: The file lists every exact-text pin and line-content rule found for O3, including the classification table rule (exact line key, category, stale-entry test), and the literal start text of the two pinned sentences of O4, so Tasks 7 to 13 can avoid or reuse them; no GitHub or network call is made.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 69f360d58d89456f559ad3de21ea75027cd72bb0
Diff against the start snapshot: NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md (240142 bytes, too large to inline; read it at .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md)
NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py (full contents, 15641 bytes):
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
constant a reader uses, that appears verbatim in a target file (raw text or prose form);
path-like literals are included, nothing is filtered but the length.
Pass B: every reader, one line each, tagged PIN or RULE. RULE means the reader's body has
a for loop (a comprehension counts), a `not in`, an `assert not`, an `is None` or a call of `re.*`: the rule lives
in that logic and a card in the record spells it out. PIN means a plain contains check.

Flag --rule-names prints only the sorted RULE names (the record's cards must equal them).
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
READ_CALLS = {"read_text", "_read", "_prose", "_text", "read_bytes", "_command_lines"}
LITERAL_CAP = 200
RE_CALLS = {"compile", "search", "match", "findall", "sub", "fullmatch"}


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


_LINES: dict[int, tuple[str, list[str]]] = {}  # the value keeps the source alive, so its id is never reused


def segment(source: str, node: ast.AST) -> str:
    """Source text of a node (same result as ast.get_source_segment, with the lines cached)."""
    if not hasattr(node, "end_lineno") or node.end_lineno is None:
        return ""
    entry = _LINES.get(id(source))
    if entry is None:
        entry = _LINES[id(source)] = (source, source.split("\n"))
    lines = entry[1]
    first, last = node.lineno - 1, node.end_lineno - 1
    if first == last:
        return lines[first].encode()[node.col_offset : node.end_col_offset].decode()
    head = lines[first].encode()[node.col_offset :].decode()
    tail = lines[last].encode()[: node.end_col_offset].decode()
    return "\n".join([head, *lines[first + 1 : last], tail])


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
            if isinstance(sub, (ast.For, ast.comprehension)) and self._mentions(sub.iter, set()):
                loop_vars.update(n.id for n in ast.walk(sub.target) if isinstance(n, ast.Name))
        # a function-local name assigned from target text (or from another such local) names target text too
        changed = True
        while changed:
            changed = False
            for sub in ast.walk(fn):
                if isinstance(sub, ast.Assign) and self._mentions(sub.value, loop_vars):
                    for tgt in sub.targets:
                        for n in ast.walk(tgt):
                            if isinstance(n, ast.Name) and n.id not in loop_vars:
                                loop_vars.add(n.id)
                                changed = True
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
            if len(text) < 8:
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


def is_rule(fn: ast.AST) -> bool:
    for sub in ast.walk(fn):
        if isinstance(sub, (ast.For, ast.AsyncFor, ast.comprehension)):
            return True
        if isinstance(sub, ast.Compare) and any(isinstance(op, (ast.NotIn, ast.IsNot)) for op in sub.ops):
            return True
        if isinstance(sub, ast.Compare) and any(
            isinstance(op, ast.Is) and isinstance(c, ast.Constant) and c.value is None
            for op, c in zip(sub.ops, sub.comparators)
        ):
            return True
        if isinstance(sub, ast.Assert) and isinstance(sub.test, ast.UnaryOp) and isinstance(sub.test.op, ast.Not):
            return True
        if (
            isinstance(sub, ast.Call)
            and isinstance(sub.func, ast.Attribute)
            and isinstance(sub.func.value, ast.Name)
            and sub.func.value.id == "re"
            and sub.func.attr in RE_CALLS
        ):
            return True
    return False


def reader_tags(analyses: list[Analysis]) -> list[tuple[str, str]]:
    return [
        (f"{an.path.relative_to(REPO)}::{name}", "RULE" if is_rule(an.funcs[name]) else "PIN")
        for an in analyses
        for name in sorted(an.readers)
    ]


READ_TEXT = re.compile(r"\b(read_text|_read|_prose|_text|read_bytes|_command_lines|open)\(")


def uncovered(analyses: list[Analysis]) -> list[str]:
    """Text-only cross-check, independent of the reader rule: functions that are not readers but whose
    body text names a target token (or a module name bound to one) and also contains a read call."""
    rows = []
    for an in analyses:
        names: set[str] = set()
        changed = True
        while changed:
            changed = False
            for name, value in an.values.items():
                if name in names:
                    continue
                text = segment(an.source, value)
                if any(t in text for t in TOKENS) or any(re.search(rf"\b{re.escape(n)}\b", text) for n in names):
                    names.add(name)
                    changed = True
        for name, fn in sorted(an.funcs.items()):
            if name in an.readers:
                continue
            body = segment(an.source, fn)
            if not READ_TEXT.search(body):
                continue
            mention = next(
                (
                    line.strip()
                    for line in body.split("\n")
                    if any(t in line for t in TOKENS) or any(re.search(rf"\b{re.escape(n)}\b", line) for n in names)
                ),
                None,
            )
            if mention is not None:
                rows.append(f"{an.path.relative_to(REPO)}::{name} | {short(mention, 120)}")
    return rows


def main() -> int:
    found = targets()
    analyses = [Analysis(p) for p in scanned_tests()]
    tags = reader_tags(analyses)
    if "--rule-names" in sys.argv[1:]:
        print("\n".join(sorted(name for name, tag in tags if tag == "RULE")))
        return 0
    if "--uncovered" in sys.argv[1:]:
        rows = uncovered(analyses)
        print("\n".join(rows) if rows else "none")
        return 0
    a_rows = pass_a(analyses, found)
    b_rows = [f"{name} {tag}" for name, tag in tags]
    readers = len(tags)
    print("## Pass A: exact-text pins (test::owner | target file | how checked | literal)")
    print("\n".join(a_rows))
    print()
    print("## Pass B: readers of target text (test or helper), tagged PIN or RULE")
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
    print(f"cap: a pass A literal is shown up to {LITERAL_CAP} characters; the full text is in the named test")
    print(f"rule names: {here} --rule-names")
    return 0


if __name__ == "__main__":
    sys.exit(main())

NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/base-lint.log (full contents, 7902 bytes):
🔍 Checking architecture policy compliance...

=== Check 1/2: Bidirectional Command ↔ Skill Links ===
  ✅ [Check 1]: adversarial → sc-adversarial-protocol
  ✅ [Check 1]: auggie-review → sc-auggie-review-protocol
  ✅ [Check 1]: brainstorm → sc-brainstorm-protocol
  ✅ [Check 1]: cleanup-audit → sc-cleanup-audit-protocol
  ✅ [Check 1]: cli-eval → sc-cli-eval-protocol
  ✅ [Check 1]: cli-portify → sc-cli-portify-protocol
  ✅ [Check 1]: graph → sc-graph-protocol
  ✅ [Check 1]: impact → sc-impact-protocol
  ✅ [Check 1]: implement → sc-implement-protocol
  ✅ [Check 1]: init-lite → sc-init-lite-protocol
  ✅ [Check 1]: issue → sc-issue-protocol
  ✅ [Check 1]: pm → sc-pm-protocol
  ✅ [Check 1]: post-release → sc-post-release-protocol
  ✅ [Check 1]: pr-submit → sc-pr-submit-protocol
  ✅ [Check 1]: recommend → sc-recommend (utility skill; no -protocol suffix)
  ✅ [Check 1]: reflect → sc-reflect-protocol
  ✅ [Check 1]: release-split → sc-release-split-protocol
  ✅ [Check 1]: review-translation → sc-review-translation-protocol
  ✅ [Check 1]: roadmap → sc-roadmap-protocol
  ✅ [Check 1]: swarm-wizard → sc-swarm-wizard-protocol
  ✅ [Check 1]: task → sc-task-protocol
  ✅ [Check 1]: tasklist → sc-tasklist-protocol
  ✅ [Check 1]: troubleshoot → sc-troubleshoot-protocol
  ✅ [Check 1]: validate-roadmap → sc-validate-roadmap-protocol
  ✅ [Check 1]: validate-tests → sc-validate-tests-protocol
  ✅ [Check 1]: workflow → sc-workflow-protocol
  ✅ [Check 2]: sc-adversarial-protocol ← adversarial.md
  ✅ [Check 2]: sc-auggie-review-protocol ← auggie-review.md
  ✅ [Check 2]: sc-brainstorm-protocol ← brainstorm.md
  ✅ [Check 2]: sc-cleanup-audit-protocol ← cleanup-audit.md
  ✅ [Check 2]: sc-cli-eval-protocol ← cli-eval.md
  ✅ [Check 2]: sc-cli-portify-protocol ← cli-portify.md
  ✅ [Check 2]: sc-graph-protocol ← graph.md
  ✅ [Check 2]: sc-impact-protocol ← impact.md
  ✅ [Check 2]: sc-implement-protocol ← implement.md
  ✅ [Check 2]: sc-init-lite-protocol ← init-lite.md
  ✅ [Check 2]: sc-issue-protocol ← issue.md
  ✅ [Check 2]: sc-pm-protocol ← pm.md
  ✅ [Check 2]: sc-post-release-protocol ← post-release.md
  ✅ [Check 2]: sc-pr-submit-protocol ← pr-submit.md
  ✅ [Check 2]: sc-reflect-protocol ← reflect.md
  ✅ [Check 2]: sc-release-split-protocol ← release-split.md
  ✅ [Check 2]: sc-review-translation-protocol ← review-translation.md
  ✅ [Check 2]: sc-roadmap-protocol ← roadmap.md
  ✅ [Check 2]: sc-swarm-wizard-protocol ← swarm-wizard.md
  ✅ [Check 2]: sc-task-protocol ← task.md
  ✅ [Check 2]: sc-tasklist-protocol ← tasklist.md
  ✅ [Check 2]: sc-troubleshoot-protocol ← troubleshoot.md
  ✅ [Check 2]: sc-validate-roadmap-protocol ← validate-roadmap.md
  ✅ [Check 2]: sc-validate-tests-protocol ← validate-tests.md
  ✅ [Check 2]: sc-workflow-protocol ← workflow.md

=== Check 3/4: Command Size Limits ===
  ⚠️  WARN [Check 3]: brainstorm.md (217 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: reflect.md (305 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: spawn.md (210 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: spec-panel.md (462 lines, warn threshold 200)
  ⚠️  WARN [Check 3]: troubleshoot.md (215 lines, warn threshold 200)

=== Check 6: Activation Section Present (for paired commands) ===
  ✅ [Check 6]: adversarial.md has ## Activation
  ✅ [Check 6]: auggie-review.md has ## Activation
  ✅ [Check 6]: brainstorm.md has ## Activation
  ✅ [Check 6]: cleanup-audit.md has ## Activation
  ✅ [Check 6]: cli-eval.md has ## Activation
  ✅ [Check 6]: cli-portify.md has ## Activation
  ✅ [Check 6]: graph.md has ## Activation
  ✅ [Check 6]: impact.md has ## Activation
  ✅ [Check 6]: implement.md has ## Activation
  ✅ [Check 6]: init-lite.md has ## Activation
  ✅ [Check 6]: issue.md has ## Activation
  ✅ [Check 6]: pm.md has ## Activation
  ✅ [Check 6]: post-release.md has ## Activation
  ✅ [Check 6]: pr-submit.md has ## Activation
  ✅ [Check 6]: reflect.md has ## Activation
  ✅ [Check 6]: release-split.md has ## Activation
  ✅ [Check 6]: review-translation.md has ## Activation
  ✅ [Check 6]: roadmap.md has ## Activation
  ✅ [Check 6]: swarm-wizard.md has ## Activation
  ✅ [Check 6]: task.md has ## Activation
  ✅ [Check 6]: tasklist.md has ## Activation
  ✅ [Check 6]: troubleshoot.md has ## Activation
  ✅ [Check 6]: validate-roadmap.md has ## Activation
  ✅ [Check 6]: validate-tests.md has ## Activation
  ✅ [Check 6]: workflow.md has ## Activation

=== Check 8: Skill Frontmatter Completeness ===
  ✅ [Check 8]: sc-adversarial-protocol frontmatter complete
  ✅ [Check 8]: sc-auggie-review-protocol frontmatter complete
  ✅ [Check 8]: sc-brainstorm-protocol frontmatter complete
  ✅ [Check 8]: sc-cleanup-audit-protocol frontmatter complete
  ✅ [Check 8]: sc-cli-eval-protocol frontmatter complete
  ✅ [Check 8]: sc-cli-portify-protocol frontmatter complete
  ✅ [Check 8]: sc-graph-protocol frontmatter complete
  ✅ [Check 8]: sc-impact-protocol frontmatter complete
  ✅ [Check 8]: sc-implement-protocol frontmatter complete
  ✅ [Check 8]: sc-init-lite-protocol frontmatter complete
  ✅ [Check 8]: sc-issue-protocol frontmatter complete
  ✅ [Check 8]: sc-pm-protocol frontmatter complete
  ✅ [Check 8]: sc-post-release-protocol frontmatter complete
  ✅ [Check 8]: sc-pr-submit-protocol frontmatter complete
  ✅ [Check 8]: sc-reflect-protocol frontmatter complete
  ✅ [Check 8]: sc-release-split-protocol frontmatter complete
  ✅ [Check 8]: sc-review-translation-protocol frontmatter complete
  ✅ [Check 8]: sc-roadmap-protocol frontmatter complete
  ✅ [Check 8]: sc-swarm-wizard-protocol frontmatter complete
  ✅ [Check 8]: sc-task-protocol frontmatter complete
  ✅ [Check 8]: sc-tasklist-protocol frontmatter complete
  ✅ [Check 8]: sc-troubleshoot-protocol frontmatter complete
  ✅ [Check 8]: sc-validate-roadmap-protocol frontmatter complete
  ✅ [Check 8]: sc-validate-tests-protocol frontmatter complete
  ✅ [Check 8]: sc-workflow-protocol frontmatter complete

=== Check 9: Protocol Naming Consistency ===
  ✅ [Check 9]: sc:adversarial-protocol ends in -protocol
  ✅ [Check 9]: sc:auggie-review-protocol ends in -protocol
  ✅ [Check 9]: sc:brainstorm-protocol ends in -protocol
  ✅ [Check 9]: sc:cleanup-audit-protocol ends in -protocol
  ✅ [Check 9]: sc:cli-eval-protocol ends in -protocol
  ✅ [Check 9]: sc-cli-portify-protocol ends in -protocol
  ✅ [Check 9]: sc:graph-protocol ends in -protocol
  ✅ [Check 9]: sc:impact-protocol ends in -protocol
  ✅ [Check 9]: sc:implement-protocol ends in -protocol
  ✅ [Check 9]: sc:init-lite-protocol ends in -protocol
  ✅ [Check 9]: sc:issue-protocol ends in -protocol
  ✅ [Check 9]: sc:pm-protocol ends in -protocol
  ✅ [Check 9]: sc:post-release-protocol ends in -protocol
  ✅ [Check 9]: sc:pr-submit-protocol ends in -protocol
  ✅ [Check 9]: sc:reflect-protocol ends in -protocol
  ✅ [Check 9]: sc:release-split-protocol ends in -protocol
  ✅ [Check 9]: sc:review-translation-protocol ends in -protocol
  ✅ [Check 9]: sc:roadmap-protocol ends in -protocol
  ✅ [Check 9]: sc:swarm-wizard-protocol ends in -protocol
  ✅ [Check 9]: sc:task-protocol ends in -protocol
  ✅ [Check 9]: sc:tasklist-protocol ends in -protocol
  ✅ [Check 9]: sc:troubleshoot-protocol ends in -protocol
  ✅ [Check 9]: sc-validate-roadmap-protocol ends in -protocol
  ✅ [Check 9]: sc:validate-tests-protocol ends in -protocol
  ✅ [Check 9]: sc:workflow-protocol ends in -protocol

=== Check 10: Workspace Suffix Blocklist ===
  ✅ [Check 10]: no *-workspace directories under .claude/skills/

=== Check 11: Contract Constant Anti-Duplication (Contract #5 + #8) ===
  ✅ [Check 11]: no contract-constant duplications

=== Checks 5/7: NEEDS DESIGN (skipped) ===
  ℹ️  Check 5 (inline protocol detection) — pending design
  ℹ️  Check 7 (activation references correct skill) — pending design

=== Summary ===
  Errors:   0
  Warnings: 5
  ✅ PASS — architecture policy compliant (5 warning(s))
Running linter...
uv run ruff check .
All checks passed!
rc=0

NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/base-format.log (full contents, 22995 bytes):
unformatted: File would be reformatted
   --> src/superclaude/examples/release-spec-template.md:142:18
    |
141 | ```python
    - {{SC_PLACEHOLDER:data_model_code}}
142 + {{SC_PLACEHOLDER: data_model_code}}
143 | ```
    |

unformatted: File would be reformatted
  --> src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md:25:49
   |
24 | ```python
   - module = importlib.import_module(os.environ.get('PLUGIN_MODULE'))
   - handler = __import__(os.getenv('HANDLER_CLASS'))
25 + module = importlib.import_module(os.environ.get("PLUGIN_MODULE"))
26 + handler = __import__(os.getenv("HANDLER_CLASS"))
27 | ```
--------------------------------------------------------------------------------
88 | ```python
   - for path in Path('handlers').glob('*.py'):
89 + for path in Path("handlers").glob("*.py"):
90 |     importlib.import_module(f"handlers.{path.stem}")
   |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md:250:40
    |
249 | # Collected for iteration
    - ALL_GATES: dict[str, GateCriteria] = {{
    -     {GATE_DICT_ENTRIES}
    - }}
250 + ALL_GATES: dict[str, GateCriteria] = {{{GATE_DICT_ENTRIES}}}
251 | ```
    |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md:23:20
    |
22  | Step(
    -     id="step-id",              # kebab-case, unique within pipeline
    -     prompt=build_X_prompt(),   # Function from prompts.py
    -     output_file="artifact.md", # Relative to work_dir
    -     gate=STEP_GATE,            # From gates.py
23  +     id="step-id",  # kebab-case, unique within pipeline
24  +     prompt=build_X_prompt(),  # Function from prompts.py
25  +     output_file="artifact.md",  # Relative to work_dir
26  +     gate=STEP_GATE,  # From gates.py
27  |     gate_mode=GateMode.BLOCKING,  # BLOCKING (default) or TRAILING
    -     timeout_seconds=600,       # Per-step timeout
    -     inputs=["dep1.md"],        # Files this step reads
    -     retry_limit=1,             # How many retries on gate failure
    -     model=None,                # None = use default from config
28  +     timeout_seconds=600,  # Per-step timeout
29  +     inputs=["dep1.md"],  # Files this step reads
30  +     retry_limit=1,  # How many retries on gate failure
31  +     model=None,  # None = use default from config
32  | )
--------------------------------------------------------------------------------
55  |     [parallel_step_a, parallel_step_b],  # Run concurrently
    -     single_step_2,                        # Waits for parallel group
56  +     single_step_2,  # Waits for parallel group
57  | ]
--------------------------------------------------------------------------------
78  |     """Pipeline-specific configuration."""
79  +
80  |     # Required: identify the input
81  |     source_path: Path
82  |
83  |     # Optional: control behavior
    -     depth: str = "standard"       # quick|standard|deep
84  +     depth: str = "standard"  # quick|standard|deep
85  |
--------------------------------------------------------------------------------
104 |     PASS = "pass"
    -     PASS_NO_SIGNAL = "pass_no_signal"    # Completed but no structured report
    -     PASS_NO_REPORT = "pass_no_report"    # Output exists but no result file
    -     INCOMPLETE = "incomplete"             # Budget exhausted
    -     HALT = "halt"                         # Step recommends stopping
    -     TIMEOUT = "timeout"                   # Hard timeout exceeded
    -     ERROR = "error"                       # Process crash
    -     SKIPPED = "skipped"                   # Skipped by config
105 +     PASS_NO_SIGNAL = "pass_no_signal"  # Completed but no structured report
106 +     PASS_NO_REPORT = "pass_no_report"  # Output exists but no result file
107 +     INCOMPLETE = "incomplete"  # Budget exhausted
108 +     HALT = "halt"  # Step recommends stopping
109 +     TIMEOUT = "timeout"  # Hard timeout exceeded
110 +     ERROR = "error"  # Process crash
111 +     SKIPPED = "skipped"  # Skipped by config
112 | ```
--------------------------------------------------------------------------------
205 |
206 +
207 | def _has_required_sections(content: str) -> bool:
--------------------------------------------------------------------------------
424 | from superclaude.cli.my_pipeline import my_pipeline_group
425 +
426 | app.add_command(my_pipeline_group)
--------------------------------------------------------------------------------
457 |
458 +
459 | @dataclass
--------------------------------------------------------------------------------
464 |
465 +
466 | # In executor:
--------------------------------------------------------------------------------
529 |     for result in prior_results[-3:]:  # Keep recent, compress older
    -         context_block += result.to_context_summary(verbose=(result == prior_results[-1]))
530 +         context_block += result.to_context_summary(
531 +             verbose=(result == prior_results[-1])
532 +         )
533 |         context_block += "\n\n"
--------------------------------------------------------------------------------
550 |             return None
    -         remaining = [r.step.id for r in self.step_results
    -                      if r.status == MyStatus.PENDING]
551 +         remaining = [
552 +             r.step.id for r in self.step_results if r.status == MyStatus.PENDING
553 +         ]
554 |         return (
--------------------------------------------------------------------------------
562 |         """Estimate turns needed to complete remaining work."""
    -         remaining_steps = sum(1 for r in self.step_results
    -                               if r.status in (MyStatus.PENDING, MyStatus.INCOMPLETE))
563 +         remaining_steps = sum(
564 +             1
565 +             for r in self.step_results
566 +             if r.status in (MyStatus.PENDING, MyStatus.INCOMPLETE)
567 +         )
568 |         return remaining_steps * 25  # Default allocation per step
--------------------------------------------------------------------------------
584 |
585 +
586 | def run_programmatic_step(step, config) -> StepResult:
--------------------------------------------------------------------------------
591 |         PROGRAMMATIC_RUNNERS[step.id](config)
    -         return StepResult(step=step, status=StepStatus.PASS,
    -                          started_at=started, finished_at=time.time())
592 +         return StepResult(
593 +             step=step,
594 +             status=StepStatus.PASS,
595 +             started_at=started,
596 +             finished_at=time.time(),
597 +         )
598 |     except Exception as e:
    -         return StepResult(step=step, status=StepStatus.FAIL,
    -                          gate_failure_reason=str(e),
    -                          started_at=started, finished_at=time.time())
599 +         return StepResult(
600 +             step=step,
601 +             status=StepStatus.FAIL,
602 +             gate_failure_reason=str(e),
603 +             started_at=started,
604 +             finished_at=time.time(),
605 +         )
606 | ```
--------------------------------------------------------------------------------
624 |         return {
    -             "none": " ", "checking": "...",
    -             "pass": "ok", "fail_deferred": "!",
    -             "remediating": "~", "remediated": "ok",
625 +             "none": " ",
626 +             "checking": "...",
627 +             "pass": "ok",
628 +             "fail_deferred": "!",
629 +             "remediating": "~",
630 +             "remediated": "ok",
631 |             "halt": "X",
    |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:99:33
    |
98  | from superclaude.pr_submit import (
    -     actionable_finding_comments, classify, classify_codex, codex_finding_comments,
    -     finding_from_comment, remap_severity, reviewer_activity, route,
99  +     actionable_finding_comments,
100 +     classify,
101 +     classify_codex,
102 +     codex_finding_comments,
103 +     finding_from_comment,
104 +     remap_severity,
105 +     reviewer_activity,
106 +     route,
107 | )
--------------------------------------------------------------------------------
117 |     review_state = classify(
    -         payload, contract, watermark=watermark, current_head_sha=expected_head,
118 +         payload,
119 +         contract,
120 +         watermark=watermark,
121 +         current_head_sha=expected_head,
122 |     )
123 |     if review_state == "findings":
124 |         selected = actionable_finding_comments(
    -             payload, contract, watermark=watermark, current_head_sha=expected_head,
125 +             payload,
126 +             contract,
127 +             watermark=watermark,
128 +             current_head_sha=expected_head,
129 |         )
--------------------------------------------------------------------------------
148 |     codex_state = classify_codex(
    -         payload, contract, watermark=codex_watermark, current_head_sha=expected_head,
149 +         payload,
150 +         contract,
151 +         watermark=codex_watermark,
152 +         current_head_sha=expected_head,
153 |     )
154 |     if codex_state == "findings":
155 |         selected = codex_finding_comments(
    -             payload, contract, watermark=codex_watermark, current_head_sha=expected_head,
156 +             payload,
157 +             contract,
158 +             watermark=codex_watermark,
159 +             current_head_sha=expected_head,
160 |         )
161 |         try:
162 |             if not selected:
    -                 raise ValueError("Codex findings signal without actionable root details")
163 +                 raise ValueError(
164 +                     "Codex findings signal without actionable root details"
165 +                 )
166 |             codex_findings = [finding_from_comment(raw) for raw in selected]
    |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md:30:23
    |
29  | ```python
    - def citation_resolves(report_path: str, fixture_root: str = None) -> AssertionResult: ...
30  + def citation_resolves(
31  +     report_path: str, fixture_root: str = None
32  + ) -> AssertionResult: ...
33  | ```
--------------------------------------------------------------------------------
42  |
43  +
44  | def check_citation_resolves(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
49  |         rel_path, line_no = m.group(1), int(m.group(2))
    -         target = (fixture_root / rel_path) if not Path(rel_path).is_absolute() else Path(rel_path)
50  +         target = (
51  +             (fixture_root / rel_path)
52  +             if not Path(rel_path).is_absolute()
53  +             else Path(rel_path)
54  +         )
55  |         if not target.exists():
56  |             failed.append(f"{rel_path}:{line_no} (file missing)")
57  |             continue
58  |         lines = target.read_text(encoding="utf-8").splitlines()
    -         window = "\n".join(lines[max(0, line_no - 6):line_no + 5])
59  +         window = "\n".join(lines[max(0, line_no - 6) : line_no + 5])
60  |         # Optional snippet check: assertion may carry expected substring
--------------------------------------------------------------------------------
66  |     total = resolved + len(failed)
    -     return (len(failed) == 0, f"{resolved}/{total} citations resolved; failures={failed}")
67  +     return (
68  +         len(failed) == 0,
69  +         f"{resolved}/{total} citations resolved; failures={failed}",
70  +     )
71  | ```
--------------------------------------------------------------------------------
83  |
84  +
85  | def check_regex_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
90  |     if matches:
    -         return True, f"Pattern {assertion['pattern']!r} found {len(matches)} match(es) in {assertion['target']}"
91  +         return (
92  +             True,
93  +             f"Pattern {assertion['pattern']!r} found {len(matches)} match(es) in {assertion['target']}",
94  +         )
95  |     return False, f"Pattern {assertion['pattern']!r} NOT found in {assertion['target']}"
--------------------------------------------------------------------------------
108 |
109 +
110 | def check_regex_absent(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
115 |     if m is None:
    -         return True, f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}"
    -     return False, f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}"
116 +         return (
117 +             True,
118 +             f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}",
119 +         )
120 +     return (
121 +         False,
122 +         f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}",
123 +     )
124 | ```
--------------------------------------------------------------------------------
137 |
138 +
139 | def check_yaml_list_contains(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
149 |     if not isinstance(node, list):
    -         return False, f"field_path {assertion['field_path']!r} is not a list (got {type(node).__name__})"
150 +         return (
151 +             False,
152 +             f"field_path {assertion['field_path']!r} is not a list (got {type(node).__name__})",
153 +         )
154 |     expected = assertion["value"]
155 |     if expected in node:
    -         return True, f"List at {assertion['field_path']} contains {expected!r}; members={node}"
    -     return False, f"List at {assertion['field_path']} missing {expected!r}; members={node}"
156 +         return (
157 +             True,
158 +             f"List at {assertion['field_path']} contains {expected!r}; members={node}",
159 +         )
160 +     return (
161 +         False,
162 +         f"List at {assertion['field_path']} missing {expected!r}; members={node}",
163 +     )
164 | ```
--------------------------------------------------------------------------------
191 |     except (TypeError, ValueError):
    -         return False, f"count field {count_field!r} not an integer: {data.get(count_field)!r}"
192 +         return (
193 +             False,
194 +             f"count field {count_field!r} not an integer: {data.get(count_field)!r}",
195 +         )
196 |     actual = len(items)
--------------------------------------------------------------------------------
220 | ```python
    - def matrix_covers_items(matrix: str, source: str, threshold: float) -> AssertionResult: ...
221 + def matrix_covers_items(
222 +     matrix: str, source: str, threshold: float
223 + ) -> AssertionResult: ...
224 | ```
--------------------------------------------------------------------------------
230 |
231 +
232 | def check_matrix_covers_items(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
238 |     source_items = {item["id"] for item in source.get("items", [])}
    -     covered = {row["item_id"] for row in matrix if row.get("status") and row["status"] != "uncovered"}
239 +     covered = {
240 +         row["item_id"]
241 +         for row in matrix
242 +         if row.get("status") and row["status"] != "uncovered"
243 +     }
244 |     if not source_items:
245 |         return False, "Source fixture has no items to cover"
246 |     ratio = len(covered & source_items) / len(source_items)
247 |     if ratio >= threshold:
    -         return True, f"Coverage {ratio:.2%} >= {threshold:.2%} ({len(covered & source_items)}/{len(source_items)} items)"
    -     return False, f"Coverage {ratio:.2%} < {threshold:.2%}; missing={sorted(source_items - covered)}"
248 +         return (
249 +             True,
250 +             f"Coverage {ratio:.2%} >= {threshold:.2%} ({len(covered & source_items)}/{len(source_items)} items)",
251 +         )
252 +     return (
253 +         False,
254 +         f"Coverage {ratio:.2%} < {threshold:.2%}; missing={sorted(source_items - covered)}",
255 +     )
256 | ```
--------------------------------------------------------------------------------
268 |
269 +
270 | def check_checkpoint_logged(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
292 | ```python
    - def deviation_class_matches(report: str, annotated_fixture: str, diff_hunk_id: str) -> AssertionResult: ...
293 + def deviation_class_matches(
294 +     report: str, annotated_fixture: str, diff_hunk_id: str
295 + ) -> AssertionResult: ...
296 | ```
--------------------------------------------------------------------------------
302 |
303 +
304 | def check_deviation_class_matches(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    -     fixture = yaml.safe_load((base_dir / assertion["annotated_fixture"]).read_text(encoding="utf-8")) or {}
    -     report = yaml.safe_load((base_dir / assertion["report"]).read_text(encoding="utf-8")) or {}
305 +     fixture = (
306 +         yaml.safe_load(
307 +             (base_dir / assertion["annotated_fixture"]).read_text(encoding="utf-8")
308 +         )
309 +         or {}
310 +     )
311 +     report = (
312 +         yaml.safe_load((base_dir / assertion["report"]).read_text(encoding="utf-8"))
313 +         or {}
314 +     )
315 |     hunk_id = assertion["diff_hunk_id"]
    -     expected = next((h["deviation_class"] for h in fixture.get("hunks", []) if h["id"] == hunk_id), None)
    -     actual = next((e["deviation_class"] for e in report.get("deviation_register", []) if e.get("hunk_id") == hunk_id), None)
316 +     expected = next(
317 +         (h["deviation_class"] for h in fixture.get("hunks", []) if h["id"] == hunk_id),
318 +         None,
319 +     )
320 +     actual = next(
321 +         (
322 +             e["deviation_class"]
323 +             for e in report.get("deviation_register", [])
324 +             if e.get("hunk_id") == hunk_id
325 +         ),
326 +         None,
327 +     )
328 |     if expected is None:
--------------------------------------------------------------------------------
345 |
346 +
347 | def check_path_exists(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
367 |
368 +
369 | def check_path_does_not_exist(assertion: dict, base_dir: Path) -> tuple[bool, str]:
--------------------------------------------------------------------------------
396 |
    - def check_falsifier_skeleton_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
397 +
398 + def check_falsifier_skeleton_present(
399 +     assertion: dict, base_dir: Path
400 + ) -> tuple[bool, str]:
401 |     case = base_dir / assertion["case_yaml"]
--------------------------------------------------------------------------------
409 |     if status == "skeleton-pending-iteration-3-fixture":
    -         return True, f"skeleton present (pending iteration-3 fixture); id={data.get('id')!r}"
410 +         return (
411 +             True,
412 +             f"skeleton present (pending iteration-3 fixture); id={data.get('id')!r}",
413 +         )
414 |     if status == "active":
--------------------------------------------------------------------------------
422 |         return True, f"active falsifier with canonical fields; id={data.get('id')!r}"
    -     return False, f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'"
423 +     return (
424 +         False,
425 +         f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'",
426 +     )
427 | ```
    |

unformatted: File would be reformatted
  --> src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md:41:31
   |
40 |     prompt=build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth),
   -     output_file=debate_file,                  # out / "debate-transcript.md"
41 +     output_file=debate_file,  # out / "debate-transcript.md"
42 |     gate=DEBATE_GATE,
   |

unformatted: File would be reformatted
  --> src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md:25:47
   |
24 | if config.input_type == "tdd":
   -     extract_prompt = build_extract_prompt_tdd(..., tool_write=config.tool_write_extract_tdd)
25 +     extract_prompt = build_extract_prompt_tdd(
26 +         ..., tool_write=config.tool_write_extract_tdd
27 +     )
28 | else:
   |

unformatted: File would be reformatted
   --> src/superclaude/skills/sc-validate-tests-protocol/SKILL.md:254:20
    |
253 |     # Boost for compound phrases
    -     if context.get('compound_phrase_matched'):
254 +     if context.get("compound_phrase_matched"):
255 |         base_confidence = min(0.95, base_confidence + 0.15)
256 |
257 |     # Reduce for vague input
    -     if context.get('vague_input') or context.get('no_keywords'):
258 +     if context.get("vague_input") or context.get("no_keywords"):
259 |         base_confidence *= 0.7
    |

unformatted: File would be reformatted
   --> src/superclaude/templates/documents/release-spec-template.md:140:18
    |
139 | ```python
    - {{SC_PLACEHOLDER:data_model_code}}
140 + {{SC_PLACEHOLDER: data_model_code}}
141 | ```
    |

unformatted: File would be reformatted
  --> tests/roadmap/fixtures/recurrence/dispatch_reachability/skipped_verification_step_case.md:44:30
   |
43 |     steps = _build_steps(config)
   -     execute_pipeline(steps)          # ends at remediate
44 +     execute_pipeline(steps)  # ends at remediate
45 |     # verify-implementation / certify terminal steps NEVER dispatched
   |

unformatted: File would be reformatted
  --> tests/roadmap/fixtures/recurrence/retry_contract/retry_loop_no_terminal_case.md:41:17
   |
40 |     id="spec-fidelity",
   -     prompt="",            # deterministic: output is f(inputs), inputs unchanged
41 +     prompt="",  # deterministic: output is f(inputs), inputs unchanged
42 |     output_file=spec_fidelity_file,
43 |     gate=SPEC_FIDELITY_GATE,
44 |     timeout_seconds=600,
   -     inputs=[spec_file, roadmap_file],   # never rewritten between attempts
   -     retry_limit=2,        # <-- futile: attempt 2 == attempt 1, byte-identical
45 +     inputs=[spec_file, roadmap_file],  # never rewritten between attempts
46 +     retry_limit=2,  # <-- futile: attempt 2 == attempt 1, byte-identical
47 | )
   |

12 files would be reformatted, 1757 files already formatted
rc=1

NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/base-full-suite.log (86613 bytes, too large to inline; read it at .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/base-full-suite.log)
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md b/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md
index 8bfa39f4..b2aec13d 100644
--- a/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md
@@ -49,9 +49,9 @@ The SKILL front matter grants programs, not scripts: `allowed-tools: Read, Grep,
 
 ### O3 pins and line-content rules the additive edits must respect
 
-How this list was produced: `./artifacts/o3-pin-scan.py` (read-only, standard library only, no network call) reads every `.md` and `.sh` file under `src/superclaude/skills/sc-pr-submit-protocol/` plus `src/superclaude/commands/pr-submit.md`, and scans `tests/pr_submit/*.py`, `tests/skills/test_worker_contract.py`, `tests/commands/test_impact_command.py`, `tests/core/test_how_we_work_routing_table.py` and every other `tests/**/*.py` that names one of the six target tokens in the script header (`sc-pr-submit-protocol`, `pr-submit.md`, `state-machine.md`, `loop-guard.md`, `ci-poll.md`, `review-retrigger.md`). A reader is a test or helper that reads target text: it reads a constant that names a target file, loops over (or comprehends over) such constants and reads the loop variable, or calls a helper that does; the write-verb audit of `tests/skills/test_worker_contract.py` is forced in because it scans whole folders. Pass A lists every string literal of 8 or more characters, held by a reader or by a constant a reader uses, that appears verbatim in a target file; path-valued literals are included and only the length filter applies. Pass B lists every reader, one line each, tagged PIN (a plain contains check) or RULE (the body has a loop or comprehension, a `not in`, an `assert not`, an `is None` or a `re.*` call, so the rule lives in logic that the literals alone do not show). Every RULE reader has one hand-written card below.
+How this list was produced: `./artifacts/o3-pin-scan.py` (read-only, standard library only, no network call) reads every `.md` and `.sh` file under `src/superclaude/skills/sc-pr-submit-protocol/` plus `src/superclaude/commands/pr-submit.md`, and scans `tests/pr_submit/*.py`, `tests/skills/test_worker_contract.py`, `tests/commands/test_impact_command.py`, `tests/core/test_how_we_work_routing_table.py` and every other `tests/**/*.py` whose text contains the substring `pr-submit` (which also covers `sc-pr-submit-protocol` and `pr-submit.md`). The six tokens in the script header (`sc-pr-submit-protocol`, `pr-submit.md`, `state-machine.md`, `loop-guard.md`, `ci-poll.md`, `review-retrigger.md`) and the module constants bound to them decide which functions are readers. A reader is a test or helper that reads target text: it reads a constant that names a target file, reads a function-local name assigned from target text (or from another such local), loops over (or comprehends over) such constants and reads the loop variable, or calls a helper that does; the write-verb audit of `tests/skills/test_worker_contract.py` is forced in because it scans whole folders. Pass A lists every string literal of 8 or more characters, held by a reader or by a constant a reader uses, that appears verbatim in a target file; path-valued literals are included and only the length filter applies. Pass B lists every reader, one line each, tagged PIN (a plain contains check) or RULE (the body has a loop or comprehension, a `not in`, an `assert not`, an `is None` or a `re.*` call, so the rule lives in logic that the literals alone do not show). Every RULE reader has one hand-written card below.
 
-Layer 1 (literals and the reader list, path literals included) is the unedited scan output: re-run it and diff. Layer 2 (rule cards) is written by hand. Check it two ways: `uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py --rule-names` must equal `rg -o '^#### RULE (\S+)' -r '$1' .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md | LC_ALL=C sort` (run the first command's output through `LC_ALL=C sort` too if the locale is not C), and each card must match its test's loop condition and constants.
+Layer 1 (literals and the reader list, path literals included) is the unedited scan output: re-run it and diff. Layer 2 (rule cards) is written by hand. Check it two ways: `uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py --rule-names` must equal `rg -o '^#### RULE (\S+)' -r '$1' .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md | LC_ALL=C sort` (run the first command's output through `LC_ALL=C sort` too if the locale is not C), and each card must match its test's loop condition and constants. The completeness of the reader list is also checked by the text-only cross-check in O3.1 below.
 
 <!-- o3-scan:begin -->
 ## Pass A: exact-text pins (test::owner | target file | how checked | literal)
@@ -376,6 +376,9 @@ tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_
 tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | COMMENTED
 tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | augmentcode[bot]
 tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | comments
+tests/pr_submit/test_edge_cases.py::test_ec15_gh_not_installed_guarded_in_poll_script | src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | command -v gh
+tests/pr_submit/test_edge_cases.py::test_ec16_base_branch_halt_documented | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Wrong origin
+tests/pr_submit/test_edge_cases.py::test_ec16_base_branch_halt_documented | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | wrong-owner
 tests/pr_submit/test_static_grep.py::SKILL_DIR | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | sc-pr-submit-protocol
 tests/pr_submit/test_static_grep.py::PR_SUBMIT_PKG | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | pr_submit
 tests/pr_submit/test_static_grep.py::RETRIGGER_SCRIPT | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | retrigger-review.sh
@@ -580,6 +583,8 @@ tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valuee
 tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution PIN
 tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates RULE
 tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root RULE
+tests/pr_submit/test_edge_cases.py::test_ec15_gh_not_installed_guarded_in_poll_script PIN
+tests/pr_submit/test_edge_cases.py::test_ec16_base_branch_halt_documented PIN
 tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments RULE
 tests/pr_submit/test_static_grep.py::test_repo_resolution_prefers_origin_over_gh_default RULE
 tests/pr_submit/test_static_grep.py::test_repo_resolution_runs_origin_first_then_falls_back RULE
@@ -673,8 +678,8 @@ target files:
   src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
   src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
   src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh
-pass A rows: 480
-pass B readers: 63
+pass A rows: 483
+pass B readers: 65
 command: uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py
 cap: a pass A literal is shown up to 200 characters; the full text is in the named test
 rule names: .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py --rule-names
@@ -1199,6 +1204,72 @@ These tests scan whole source folders through constants that name no pr-submit t
 - **Files:** `src/superclaude/skills/*/SKILL.md` except `sc-graph-protocol`.
 - **Rule:** the text `sc:graph-protocol` must not occur in them (T9 and T10 never write it).
 
+### O3.1 cross-check
+
+The reader rule of the scan could miss a reader, so completeness is also checked by a second method that does not use the rule. `--uncovered` is text-only: it lists every function of a scanned test file that is not in Pass B, whose body text names a target token (or a module name bound to one) and that contains a read call. Its unedited output, with its command (`uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py --uncovered`):
+
+```text
+tests/pr_submit/test_codex_reviews.py::fake_gh | [str(SCRIPTS / script), *args],
+tests/pr_submit/test_conflict_scripts.py::run_evidence | str(EVIDENCE),
+tests/pr_submit/test_cosmos_poll.py::adapter | args = [str(SCRIPTS / script), "--pr", "266", "--repo", REPO]
+tests/pr_submit/test_static_grep.py::test_ci_poll_script_rejects_gh_without_checks_json | str(SKILL_DIR / "scripts" / "poll-ci-checks.sh"),
+tests/unit/test_cli_install.py::_install_hooks | assert "session-init.sh" in _PACKAGE_RESOURCES["scripts"]
+```
+
+Each row above is not a text pin, for the reason given:
+
+- `tests/pr_submit/test_codex_reviews.py::fake_gh`: runs a script from a fake `gh` and returns its result; it reads no target text.
+- `tests/pr_submit/test_conflict_scripts.py::run_evidence`: runs `collect-conflict-evidence.sh` in a temporary repository; the text rules of that script are on the card for `test_evidence_script_static_rules`.
+- `tests/pr_submit/test_cosmos_poll.py::adapter`: runs the poll script against a fake `gh`; it reads no target text.
+- `tests/pr_submit/test_static_grep.py::test_ci_poll_script_rejects_gh_without_checks_json`: runs `poll-ci-checks.sh` with a fake `gh`; it asserts the script's runtime message `gh pr checks --json` and exit code 2, which is the same text as the exempt `die` line in the `test_gh_command_lines_are_repo_scoped` card; no plan task edits that script.
+- `tests/unit/test_cli_install.py::_install_hooks`: installs hook files; it names no pr-submit file (the matched name is the package resource list).
+
+The files that name `pr-submit`, as listed by `rg` (command and unedited output), to compare with the `scanned test files` list in the footer of the scan block above:
+
+```text
+$ rg --sort path -l -e 'sc-pr-submit-protocol' -e 'pr-submit' tests --glob '*.py'
+tests/commands/test_impact_command.py
+tests/core/test_how_we_work_routing_table.py
+tests/pr_submit/test_codex_reviews.py
+tests/pr_submit/test_conflict_e2e.py
+tests/pr_submit/test_conflict_scripts.py
+tests/pr_submit/test_conflict_sync_protocol.py
+tests/pr_submit/test_conflicts_core.py
+tests/pr_submit/test_contract_setup_diagnosis.py
+tests/pr_submit/test_contract_setup_pr_submit_integration.py
+tests/pr_submit/test_cosmos_poll.py
+tests/pr_submit/test_cosmos_protocol.py
+tests/pr_submit/test_detection_contract.py
+tests/pr_submit/test_edge_cases.py
+tests/pr_submit/test_pre_pr_checks.py
+tests/pr_submit/test_silence.py
+tests/pr_submit/test_static_grep.py
+tests/skills/test_worker_contract.py
+tests/unit/test_cli_install.py
+```
+
+```text
+$ rg --sort path -c -e 'sc-pr-submit-protocol' -e 'pr-submit' tests --glob '*.py'
+tests/commands/test_impact_command.py:3
+tests/core/test_how_we_work_routing_table.py:2
+tests/pr_submit/test_codex_reviews.py:2
+tests/pr_submit/test_conflict_e2e.py:1
+tests/pr_submit/test_conflict_scripts.py:11
+tests/pr_submit/test_conflict_sync_protocol.py:3
+tests/pr_submit/test_conflicts_core.py:2
+tests/pr_submit/test_contract_setup_diagnosis.py:3
+tests/pr_submit/test_contract_setup_pr_submit_integration.py:2
+tests/pr_submit/test_cosmos_poll.py:1
+tests/pr_submit/test_cosmos_protocol.py:1
+tests/pr_submit/test_detection_contract.py:3
+tests/pr_submit/test_edge_cases.py:2
+tests/pr_submit/test_pre_pr_checks.py:1
+tests/pr_submit/test_silence.py:1
+tests/pr_submit/test_static_grep.py:3
+tests/skills/test_worker_contract.py:132
+tests/unit/test_cli_install.py:21
+```
+
 Rules that are not text pins and that the block does not show:
 
 - `tests/skills/test_worker_contract.py`: `WRITE_VERB_RE` matches whole-word `gh pr`, `gh api` and the git write verbs on every line under `src/superclaude/{skills,commands,agents}` (scripts included). Each hit must be a key of `WRITE_VERB_CLASSIFICATION`: (repo-relative path, verb text joined with `+` when a line has several, exact stripped line) with a category (`never-worker` for pr-submit, with the standard reason text) and a one-line reason. `test_every_write_verb_hit_is_classified` fails on an unclassified hit; `test_classification_table_has_no_stale_entries` fails when a classified line no longer exists, so the existing Wave 0, Wave 0 head binding, Wave 0 conflict check, Wave 6 and Wave 8a lines of `SKILL.md` are exact keys and must stay byte-identical; new Wave bullets are new physical lines.

diff --git a/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py b/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py
index a0a9d9fd..4da828b8 100644
--- a/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py
@@ -158,6 +158,17 @@ class Analysis:
         for sub in ast.walk(fn):
             if isinstance(sub, (ast.For, ast.comprehension)) and self._mentions(sub.iter, set()):
                 loop_vars.update(n.id for n in ast.walk(sub.target) if isinstance(n, ast.Name))
+        # a function-local name assigned from target text (or from another such local) names target text too
+        changed = True
+        while changed:
+            changed = False
+            for sub in ast.walk(fn):
+                if isinstance(sub, ast.Assign) and self._mentions(sub.value, loop_vars):
+                    for tgt in sub.targets:
+                        for n in ast.walk(tgt):
+                            if isinstance(n, ast.Name) and n.id not in loop_vars:
+                                loop_vars.add(n.id)
+                                changed = True
         for sub in ast.walk(fn):
             if not isinstance(sub, ast.Call):
                 continue
@@ -281,6 +292,44 @@ def reader_tags(analyses: list[Analysis]) -> list[tuple[str, str]]:
     ]
 
 
+READ_TEXT = re.compile(r"\b(read_text|_read|_prose|_text|read_bytes|_command_lines|open)\(")
+
+
+def uncovered(analyses: list[Analysis]) -> list[str]:
+    """Text-only cross-check, independent of the reader rule: functions that are not readers but whose
+    body text names a target token (or a module name bound to one) and also contains a read call."""
+    rows = []
+    for an in analyses:
+        names: set[str] = set()
+        changed = True
+        while changed:
+            changed = False
+            for name, value in an.values.items():
+                if name in names:
+                    continue
+                text = segment(an.source, value)
+                if any(t in text for t in TOKENS) or any(re.search(rf"\b{re.escape(n)}\b", text) for n in names):
+                    names.add(name)
+                    changed = True
+        for name, fn in sorted(an.funcs.items()):
+            if name in an.readers:
+                continue
+            body = segment(an.source, fn)
+            if not READ_TEXT.search(body):
+                continue
+            mention = next(
+                (
+                    line.strip()
+                    for line in body.split("\n")
+                    if any(t in line for t in TOKENS) or any(re.search(rf"\b{re.escape(n)}\b", line) for n in names)
+                ),
+                None,
+            )
+            if mention is not None:
+                rows.append(f"{an.path.relative_to(REPO)}::{name} | {short(mention, 120)}")
+    return rows
+
+
 def main() -> int:
     found = targets()
     analyses = [Analysis(p) for p in scanned_tests()]
@@ -288,6 +337,10 @@ def main() -> int:
     if "--rule-names" in sys.argv[1:]:
         print("\n".join(sorted(name for name, tag in tags if tag == "RULE")))
         return 0
+    if "--uncovered" in sys.argv[1:]:
+        rows = uncovered(analyses)
+        print("\n".join(rows) if rows else "none")
+        return 0
     a_rows = pass_a(analyses, found)
     b_rows = [f"{name} {tag}" for name, tag in tags]
     readers = len(tags)
Earlier blocking findings of this start (empty on the first review): F4.1 sev=blocking trigger=B1 ac=T1.AC3 at=tests/pr_submit/test_edge_cases.py:252 anchor="lists every exact-text pin and line-content rule found for O3" chk=y,y,n,n family=o3-pin-completeness fix=Add two lines to the PIN or RULE inventory, or have the scan detect function-local path variables. (1) `test_ec15_gh_not_installed_guarded_in_poll_script` requires `command -v gh` in `scripts/poll-augment-review.sh`. (2) `test_ec16_base_branch_halt_documented` requires `SKILL.md` to contain `Wrong origin`, `behind` or `wrong-owner`. Then reword the "Pass B lists every reader" sentence in the O3 intro paragraph to state the scan's limit. covers="lists every exact-text pin and line-content rule found for O3" first=A4 origin=new: Both tests read target text through a function-local `script` or `skill` variable. `_reads_target` only follows module-level constants and loop variables, so neither shows in the Pass B reader list. They are absent from both Pass A and Pass B, although the O3 intro paragraph of the record says Pass B "lists every reader". Neither pin can be broken by an additive edit, so the harm is small, but the inventory and its completeness claim are wrong.
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
