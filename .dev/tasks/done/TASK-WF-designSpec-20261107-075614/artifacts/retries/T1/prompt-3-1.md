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
Diff against the start snapshot: NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md (183795 bytes, too large to inline; read it at .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md)
NEW FILE .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py (full contents, 11937 bytes):
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
index 9552654b..625fb0b7 100644
--- a/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md
@@ -49,17 +49,817 @@ The SKILL front matter grants programs, not scripts: `allowed-tools: Read, Grep,
 
 ### O3 pins and line-content rules the additive edits must respect
 
-Found by grepping `tests/` for every reader of the pr-submit skill, ref, script and command files (`sc-pr-submit-protocol`, `pr-submit.md`, `pr_submit`); the final full-suite run of Task 13 is the backstop for anything a text search cannot see.
+How this list was produced: `./artifacts/o3-pin-scan.py` (read-only, standard library only, no network call) reads every `.md` and `.sh` file under `src/superclaude/skills/sc-pr-submit-protocol/` plus `src/superclaude/commands/pr-submit.md`, and scans `tests/pr_submit/*.py`, `tests/skills/test_worker_contract.py`, `tests/commands/test_impact_command.py`, `tests/core/test_how_we_work_routing_table.py` and every other `tests/**/*.py` that names `sc-pr-submit-protocol` or `pr-submit`. A reader is a test or helper that reads target text (the script header states the rule; the write-verb audit of `tests/skills/test_worker_contract.py` is forced in because it scans whole folders). Pass A lists every string literal of 8 or more characters, held by a reader or a constant a reader uses, that appears verbatim in a target file; Pass B lists every reader with the source of each assert and regular-expression call (so absence checks and line rules are included).
+
+Complete by construction: re-run the command in the footer and diff against this block.
+
+<!-- o3-scan:begin -->
+## Pass A: exact-text pins (test::owner | target file | how checked | literal)
+tests/commands/test_impact_command.py::_SKILLS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
+tests/commands/test_impact_command.py::_IMPACT_CALLERS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | sc-pr-submit-protocol
+tests/commands/test_impact_command.py::_IMPACT_CALLERS | src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | sc-troubleshoot-protocol
+tests/commands/test_impact_command.py::_IMPACT_CALLERS | src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | sc-auggie-review-protocol
+tests/commands/test_impact_command.py::test_impact_callers_wired | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | in | Skill sc:impact-protocol
+tests/commands/test_impact_command.py::test_impact_callers_wired | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | in | `status: blocked|failed` counts as `graph:absent`
+tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .get() | allowed-tools
+tests/commands/test_impact_command.py::test_impact_callers_wired | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | --caller
+tests/pr_submit/test_codex_reviews.py::_skill_gate | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | contract
+tests/pr_submit/test_codex_reviews.py::_skill_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | pushed_sha
+tests/pr_submit/test_codex_reviews.py::_skill_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | watermark
+tests/pr_submit/test_codex_reviews.py::_skill_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | codex_watermark
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | compare | findings
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | head_sha
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | dedup_groups(findings)
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | routes at its members' highest remapped tier
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | `fix_applied` is recorded for **every** member's `fix_key`
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | **every verified member's thread** is replied to and resolved
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | "flagged by: augment, codex"
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | covers **only the reviewers re-triggered in this cycle**
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | at least one\nre-triggered reviewer reaches `done`
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | reviewer_incomplete{reviewer, phase: "rereview"}
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | plus any merged Codex `findings`
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | set member | rebuild_state()["absent_reviewers"]
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | pending_retriggers(
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | rereview_requested{cycle_id, reviewer, timestamp}
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | reuse the `cycle_id` of the dangling push record
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | poll_result
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | review_detected
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | findings_normalized
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | finding_verified
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | finding_unverified
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | route_decision
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | reply_posted
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | thread_resolved
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | rereview_requested
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | other | codex_state
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | codex_routes
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | other | activity
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | other | codex_state
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | .index() | pending_retriggers
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | before the S5 poll
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | codex_findings
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | Every event that concerns one reviewer
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | .index() | On `--resume`
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | **Resume of a re-triggered cycle:**
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | other | codex_findings
+tests/pr_submit/test_conflict_scripts.py::SKILL_DIR | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | sc-pr-submit-protocol
+tests/pr_submit/test_conflict_scripts.py::ALL_EVIDENCE_FILES | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | worktree
+tests/pr_submit/test_conflict_scripts.py::ALL_EVIDENCE_FILES | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | diff-ours.txt
+tests/pr_submit/test_conflict_scripts.py::ALL_EVIDENCE_FILES | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | diff-theirs.txt
+tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | .startswith() | #!/usr/bin/env bash\n
+tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | in | \nset -u -o pipefail\n
+tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | .startswith() | #!/usr/bin/env bash\n
+tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | in | \nset -u -o pipefail\n
+tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | .startswith() | #!/usr/bin/env bash\n
+tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | in | \nset -u -o pipefail\n
+tests/pr_submit/test_conflict_scripts.py::SKILL_DIR | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
+tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | in | \nLIMIT_SECONDS=60\n
+tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | set member | --base-sha
+tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | --merge-base
+tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | .index() | if [ "$EVIDENCE_MODE" -eq 1 ]; then
+tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | .index() | gh pr checks --repo
+tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | ls-files
+tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | ls-files
+tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | .replace() | \nLIMIT_SECONDS=60\n
+tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | #!/usr/bin/env bash\n
+tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | set member | ls-files
+tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | repos/${REPO}/
+tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | other | \nLIMIT_SECONDS=
+tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | sc-pr-submit-tmp
+tests/pr_submit/test_conflict_sync_protocol.py::PUSH_LINE | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | git push origin <target_sha>:<HEAD_BRANCH>
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_DIR | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | sc-pr-submit-protocol
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git checkout --ours -- uv.lock
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | uv lock --check
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git add -- uv.lock
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | merge_parent_ok(<parents>, pre_push_sha, base_sha)
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git merge-base --is-ancestor <base_sha> origin/<base>
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | The deterministic core DECIDES
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | set member | evaluate_sync_decision
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | sync_started
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | reason `pr_conflicting`
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | set member | --evidence-sha
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | expect_checks
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | push_rejected
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | push_failed
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git revert -m 1 <merge_sha>
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | Nothing was changed and nothing was pushed.
+tests/pr_submit/test_conflict_sync_protocol.py::MECHANICAL_PINS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | never stash
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | merge --no-commit --no-ff <base_sha>
+tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | evidence-validator
+tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | One revision pass
+tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | one sentence
+tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | high-suspicion
+tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | configured reviewers
+tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | base_authored
+tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git add -- <path>
+tests/pr_submit/test_conflict_sync_protocol.py::INTENT_PINS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git rm -- <path>
+tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | root_cause
+tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | ours_intent
+tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | theirs_intent
+tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | resolution
+tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | behavior_after
+tests/pr_submit/test_conflict_sync_protocol.py::RECORD_FIELDS | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | set member | evidence
+tests/pr_submit/test_conflict_sync_protocol.py::_PRE_EXISTING_VALIDATOR_LINES | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | read-only evidence-validator before diagnosis or edits.
+tests/pr_submit/test_conflict_sync_protocol.py::_PRE_EXISTING_VALIDATOR_LINES | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent
+tests/pr_submit/test_conflict_sync_protocol.py::COMMAND_MD | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | other | commands
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | ## Merge-conflict handling
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | `--conflict-max-tier` (default 0)
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | before the first review
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | at most one conflict cycle per run
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | uncommitted merge in progress
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | no review round
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | not a sandbox
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation | src/superclaude/commands/pr-submit.md | in | Skill sc:pr-submit-protocol
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | **Step 5. Resolve.**
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | **Step 6
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | <python> -I -c 'import json, sys; from superclaude.pr_submit.conflicts
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | `uv run --no-sync python`
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | never use plain `uv run`
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | **Step 3. Write-ahead.**
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | other | **Step 4.
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | conflict_attempt(<run-log events>, cycle_id)
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | cycle_dir := <output-dir>/sync/<cycle_id>/a<attempt>/
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | in | --out <cycle_dir><n>/
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | <cycle_dir>resolution.md
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | in | `<cycle_dir>` (this attempt only) as `output_dir`
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E1'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `--conflict-max-tier {0,1,2}` | No (default 0) | Highest merge-conflict tier the skill may act on: 0 (default) detect and report only, 1 also regenerate a conflicted root `uv.lock` (Tier 1, opt-in b [+144 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E2'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | **STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's\n`owner/repo`, parsed from `git remote get-url origin`): a wrong origin, or a returned URL whose `owne [+241 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E3'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `push_count` | int | Landed fix, CI and Tier 2 merge pushes (`kind` on every push record; Tier 1 sync pushes are counted in `sync_push_count`); `<= max_rounds + 1` with the fallback's single push; 0 [+12 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E3'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `sync_tier` | int or null | Highest merge-conflict tier seen this run (0 to 3; null when it could not be classified). |
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E3'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `sync_outcome` | enum | `none` / `report_only` / `left_in_progress` / `pushed` / `aborted` / `halted`. |
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E3'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | `sync_push_count` | int | Landed Tier 1 sync pushes (`kind: "sync"`, at most `SYNC_CAP = 1`); never counted in `push_count`. |
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E4'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Wave 0c: (L1+) conflict check + report ← loads refs/conflict-mechanical.md ONLY when the probe runs
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E4'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | C-initial: (L3, Tier 2) merge cycle before the first review poll ← loads refs/conflict-mechanical.md + refs/conflict-intent.md
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E4'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Wave 8a: (L1+) act on a conflict before the CI wait ← loads refs/conflict-mechanical.md ONLY when the probe runs
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E5'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not rebase and does not halt: the branch is already published when `gh pr create` runs, so report how many commits it is be [+538 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E6'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - **Wave 0 conflict check (L1+ only; L0 skips it):** after the head binding, read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus` (re-read an `UNKNOWN` up to 3 times, 10  [+521 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E7'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | `--monitor 0` remains no-monitor. **C-initial (L3, Tier 2, only when Wave 0 planned it under `--conflict-max-tier 2`):** after arming and before the first review poll, load `refs/conflict-intent.md` a [+156 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E8'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | load `refs/ci-poll.md`, then run Wave 8a (below) before the CI poll loop. These are
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | classify_checks(payload, wait_sha=<sha at flip or last push>, expect_checks=<the value recorded for that push, else false>)
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | without fetching logs, editing, or pushing a fix; the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is not a fix.
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | so this push too carries only the cycle's one fix commit; its triad passes `push_kind="ci"`, `review_terminal` and `expect_checks=True`.
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E9'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Only parsed empty required **and** all-checks lists, with `expect_checks` false, prove there are no Actions; with `expect_checks` true an empty list is `polling`, and expiry is the CI timeout with rea [+34 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E10'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave 8):** read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRep [+952 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E11'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - Detect merge conflicts at Wave 0 (L1+), report the tier and plan before any edit, and resolve only within `--conflict-max-tier` and the ordinal ceiling, publishing a resolution only as one merge com [+50 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E11'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | - Rebase a published PR head (at L1+ the create path no longer rebases), stash, take one side for a whole tree, commit a merge without `scripts/finish-merge.sh`, or push a merge commit whose parents a [+73 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | Wrong origin / wrong-owner URL | HALT; instruct operator to close the misrouted PR (FM-11). |
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | Behind base branch (create path at L1+, or `--pr`) | Tier 0 report ("<N> commits behind"); no rebase, no halt. At L0 the create path still rebases. |
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | A merge, rebase, cherry-pick, revert or sequencer operation is in progress (L1+) | `terminal_halted`, reason `foreign_op_in_progress`, before anything is created; finish or abort that operation your [+20 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | Merge conflict that needs a human (Tier 3: submodule, symlink, mode change, protected or migration path, binary, lock or generated file without a rule, more than 8 text files, unclassifiable) | L3:  [+181 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E12'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | | A conflict cycle stops (dirty tree, foreign merge, guard, finish gate, VAL, rejected or failed push) | `terminal_halted` with the reason from `refs/conflict-mechanical.md` (`merge_preflight_dirty`,  [+139 chars]
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_EDITS['E13'] | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | (push if you are ahead; `git pull --ff-only` if you are behind; this skill never rewrites a published branch)
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | with `--pr <N>`, at any level, do not rebase
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | rebase if behind `origin/<base>`
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | pr_head_ok(<local branch>, pre_push_sha,
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | push_parent_ok(<parents>, pre_push_sha)
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | The deterministic core DECIDES
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | then set `pre_push_sha := target_sha`
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/commands/pr-submit.md | in | push any commit besides the cycle's one fix commit
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | the commit to push must have exactly one parent, that same SHA
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | The parent check applies only when the cycle applied edits
+tests/pr_submit/test_conflict_sync_protocol.py::SKILL_DIR | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
+tests/pr_submit/test_conflict_sync_protocol.py::COMMAND_MD | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | **Step 1. Head check.**
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md | set member | sync_started
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | merge_preflight_ok
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | **Step 10(a). Head re-read.**
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | merge_parent_ok(<parents>, pre_push_sha, base_sha)
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | --is-ancestor
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | The deterministic core DECIDES
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | set member | --precheck
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | lock_trust_findings
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | sync_tier3
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | git checkout --ours -- uv.lock
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | uv lock\n
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | uv lock --check
+tests/pr_submit/test_conflict_sync_protocol.py::test_trust_limit_is_documented_in_the_refs_skill_and_command | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | collaborators you trust with your credentials
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_record_fields_in_order | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | .index() | ## 6. The resolution record
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_record_fields_in_order | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | set member | `## <path>`
+tests/pr_submit/test_conflict_sync_protocol.py::test_skill_replaced_text_is_gone | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | **Wave 0 head binding (L1+ only
+tests/pr_submit/test_conflict_sync_protocol.py::test_skill_replaced_text_is_gone | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 0 conflict check
+tests/pr_submit/test_conflict_sync_protocol.py::test_skill_keeps_one_python_block | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .startswith() | ```python
+tests/pr_submit/test_conflict_sync_protocol.py::test_allowed_tools_cover_every_program | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | .startswith() | scripts/
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 6 (L3 only):**
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 6b
+tests/pr_submit/test_conflict_sync_protocol.py::test_intent_and_validator_lines_say_tier_2 | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | not in | evidence-validator
+tests/pr_submit/test_conflict_sync_protocol.py::test_allowed_tools_cover_every_program | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .startswith() | allowed-tools:
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | .parametrize() | resolved
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | .parametrize() | watermark
+tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | contract
+tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | pushed_sha
+tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | watermark
+tests/pr_submit/test_cosmos_protocol.py::attended_gate | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | codex_watermark
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | isResolved
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | set member | classify
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | actionable_finding_comments
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | finding_from_comment
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | remap_severity
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | compare | findings
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | isResolved
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | head_sha
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | .setattr() | classify
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | .setattr() | finding_from_comment
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | comments_ok
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | reviews_ok
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | threads_ok
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | head_sha
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | set member | comments
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | compare | findings
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | isResolved
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | databaseId
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | other | severity_hint
+tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | other | isResolved
+tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | compare | findings
+tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | compare | unverified
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | compare | auggie review
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | classify
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | other | actionable_finding_comments
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | watermark
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | current_head_sha
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | compare | unverified
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | report-only
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | has_findings
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | findings_count
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
+tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | other | review_state
+tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | other | findings
+tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | set member | report-only
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | RunConfig.rereview_outcome
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | optimistic legacy default
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | evidence-validator
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | without\nresetting elapsed time
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Never pass `review_state="findings"` with an empty `findings` list
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | not a stable\npublic API
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | documentary fields, not runtime parser rules
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | lower bound
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | strictly\nnewer than `watermark`
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | observed_at
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | reviews_ok
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | comments_ok
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | threads_ok
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | set member | comments(first:1)
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | set member | pageInfo{hasNextPage endCursor}
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | set member | all three flags false
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | body="auggie review"
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | payload.head_sha == pushed_sha
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | strictly newer
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | finding_from_comment(raw)
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | ValueError
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | LF or CRLF
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md | set member | verification_status="unverified"
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh | set member | --thread-id
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | no path/line lookalike match
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | idempotency_skip BEFORE reply
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | hasNextPage:false
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | set member | thread.isResolved:true
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | augmentcode[bot]
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | augmentcode
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | submitted_at
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | set member | commit_id
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md | set member | COMMENTED
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | set member | augmentcode[bot]
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | comments
+tests/pr_submit/test_static_grep.py::SKILL_DIR | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md | other | sc-pr-submit-protocol
+tests/pr_submit/test_static_grep.py::PR_SUBMIT_PKG | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | other | pr_submit
+tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | other | --depth quick --remediation-offer
+tests/pr_submit/test_static_grep.py::PR_SUBMIT_PKG | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
+tests/pr_submit/test_static_grep.py::AUGGIE_REVIEW_CMD | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | other | commands
+tests/pr_submit/test_static_grep.py::test_t105_runtime_repo_pin | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | git remote get-url origin
+tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md | in | check_idempotent("silence_rerequest_invoked"
+tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | in | rerequested=
+tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md | in | rerequested_at=
+tests/pr_submit/test_static_grep.py::test_t1105_retrigger_token_in_script_not_core | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | auggie review
+tests/pr_submit/test_static_grep.py::test_t1105_retrigger_token_in_script_not_core | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | not in | auggie review
+tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | set member | --remediation-offer
+tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | gh api "repos/${REPO}/issues/${PR}/comments"
+tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | gh api "repos/${REPO}/pulls/${PR}/comments"
+tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | ($issue_comments[0] // []) + ($inline_comments[0] // [])
+tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | --slurpfile issue_comments
+tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh | in | --slurpfile inline_comments
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | after `gh pr create`, or on `--pr <N>` attach
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | --json headRefName,headRefOid,isCrossRepository
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | set member | pr_head_ok(
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | HEAD_BRANCH := headRefName
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | pre_push_sha := headRefOid
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | `--resume` repeats this binding
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | pr_branch_ok(
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | Do not close the PR.
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | its `target_sha` when the push landed (Branch A)
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | set member | the re-driven push first runs the Wave 6 pre-push head guard
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | with `--pr <N>`, at any level, do not rebase
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | rebase if behind `origin/<base>`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | rebase if behind `origin/<base>` only at L0
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Being behind the base branch is not a STOP at L1+
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | | Wrong origin / wrong-owner URL |
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | | Behind base branch (create path at L1+, or `--pr`) |
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | reason `pr_head_mismatch`; nothing pushed; do NOT close the PR
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | Pre-push head guard, before `push_decision`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | in | pr_head_ok(<local branch>, pre_push_sha,
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | never local HEAD
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | target_branch := HEAD_BRANCH
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | then set `pre_push_sha := target_sha`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | push_parent_ok(<parents>, pre_push_sha)
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | `terminal_halted` (reason `push_range_mismatch`)
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | | The commit to push is not exactly one commit on top of the PR head
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | after Branch A, the guard's parent check stops the next push
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | **Fix commit:**
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | commit all of them as exactly one commit
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Next, when the cycle applied edits (a zero-edit cycle has no fix commit
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | An L3 CI push runs the Wave 6 pre-push head guard and push triad with `target_branch := HEAD_BRANCH`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | runs the guard's parent check (`push_parent_ok`)
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | `terminal_halted` (reason `fix_commit_failed`)
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | A crash re-drive (Branch B) skips this step
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Branch B: skip the Wave 6 fix commit, set `target_sha` from the record
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | pre-push head guard with the record's `pre_push_sha`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | | The fix touched a file with the operator's own pending changes, the fix commit fails, or HEAD does not advance
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | staging only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | committing with `git commit --only -- <paths>`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Before the cycle's first edit, record the operator's pending files (`git status --porcelain=v1 -z --untracked-files=all`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Before staging anything (before the `git add` above), if a path to commit is in `OPERATOR_PENDING`
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | The fix touched files that had your own uncommitted changes: <paths>
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | separate them by hand (do not discard the files)
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | A halted cycle replies to and resolves no thread.
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | The fix commit failed (<error>). Nothing was pushed
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Fix the cause, then either commit and push the fix yourself
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | make your checkout equal the new PR head, then re-run
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | When this cycle made a fix commit, the message adds:
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | This cycle's fixes are in local commit <target_sha>
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | the commit to push must have exactly one parent, that same SHA
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | The parent check applies only when the cycle applied edits
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/commands/pr-submit.md | in | push any commit besides the cycle's one fix commit
+tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Force-push (`--force`, `--force-with-lease`, or a `+` refspec)
+tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is not a fix
+tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | never an additional fix or fix push. The single exception is the one Tier 1 sync push (5.2d), which is not a fix.
+tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception | src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md | in | the one Tier 1 sync push of Wave 8a is the only push allowed here, and it is not a fix
+tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`)
+tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post
+tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | in | Next, when the cycle applied edits (a zero-edit cycle has no fix commit
+tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | in | The parent check applies only when the cycle applied edits
+tests/pr_submit/test_static_grep.py::SKILL_DIR | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
+tests/pr_submit/test_static_grep.py::AUGGIE_REVIEW_CMD | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
+tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | not in | --no-post-pr
+tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | not in | --auggie-model
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | .index() | The deterministic core DECIDES
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | .index() | pr_head_ok(<local branch>, pre_push_sha,
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | (reason `pr_head_mismatch`)
+tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .search() | git push origin <target_sha>:<target_branch>
+tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md | .startswith() | > Skill sc:auggie-review-protocol
+tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh | in | gh pr view
+tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md, src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | not in | comments
+tests/pr_submit/test_static_grep.py::test_repo_resolution_sed_handles_all_url_forms | src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh | other | , expected
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | **Wave 0 head binding (L1+ only
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 1
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 6 (L3 only):**
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 6b
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 8 (L1+
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 4:**
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 5
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/commands/pr-submit.md | .index() | **Will Not:**
+tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | ## Will Not Do
+tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | - **Wave 6 (L3 only):**
+tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | .index() | \n- **Wave 6b
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md | other | commands
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | other | superclaude
+tests/pr_submit/test_static_grep.py::test_repo_resolution_sed_handles_all_url_forms | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | git remote get-url origin
+tests/pr_submit/test_static_grep.py::test_repo_resolution_prefers_origin_over_gh_default | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | git remote get-url origin
+tests/pr_submit/test_static_grep.py::test_repo_resolution_prefers_origin_over_gh_default | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh | in | gh repo view --json nameWithOwner
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+151 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+157 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+55 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+48 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+103 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/SKILL.md', 'gh pr', [+80 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubri [+248 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-crash-recovery/SKILL.md', 'git commit', '- [+184 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-crash-recovery/refs/investigators.md', 'gi [+47 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/SKILL.md', 'git commit+gi [+1351 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/SKILL.md', 'git add', '** [+213 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/SKILL.md', 'git add', '-  [+93 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/SKILL.md', 'git add', '** [+299 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+300 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+102 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+520 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+207 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+212 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md', [+283 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-reflect-protocol/refs/promotion-adapters.m [+258 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md', 'gh api', [+889 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md', 'gh api', [+241 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md', 'gh api', [+286 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/commands/auggie-review.md', 'gh pr', '- **Remote PR* [+60 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/agents/issue-worker-t1.md', 'gh pr+gh api', '- **Rea [+658 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/agents/issue-worker-t2.md', 'gh pr+gh api', '- **Rea [+658 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/agents/issue-worker-t3.md', 'gh api', '- **Read-only [+512 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/agents/issue-worker-t3.md', 'gh api+gh pr', '1. **Cl [+1044 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/SKILL.md', 'gh api', '- Eve [+160 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/refs/claim.md', 'gh api', ' [+146 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/refs/claim.md', 'gh api', ' [+216 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/refs/claim.md', 'gh pr', '- [+275 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+tests/skills/test_worker_contract.py::WRITE_VERB_CLASSIFICATION[('src/superclaude/skills/sc-issue-protocol/refs/create.md', 'gh api',  [+269 chars]] | src/superclaude/commands/pr-submit.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh, src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh | set member | read-only
+
+## Pass B: readers of target text (test or helper), with their asserts and regex calls
+tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill
+    assert: assert "Skill" in tools, rel
+tests/commands/test_impact_command.py::test_impact_callers_wired
+    assert: assert "Skill sc:impact-protocol" in text, rel
+    assert: assert f"--caller {caller}" in text, rel
+    assert: assert "`status: blocked|failed` counts as `graph:absent`" in text, rel
+tests/pr_submit/test_codex_reviews.py::_skill_gate
+    assert: assert len(blocks) == 1, "keep one executable snapshot gate"
+    regex: re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_adds_the_codex_part_on_the_same_snapshot
+    assert: assert gated["codex_state"] == "findings"
+    assert: assert [f.reviewer for f in gated["codex_findings"]] == ["codex"] * 3
+    assert: assert gated["codex_routes"] == ["--fix"] * 3
+    assert: assert gated["activity"] == {"augment": True, "codex": True}
+    assert: assert gated["review_state"] == classify(findings336, CONTRACT)
+tests/pr_submit/test_codex_reviews.py::test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules
+    assert: assert _skill_gate(findings336, pushed_sha="b" * 40)["codex_state"] == "polling"
+    assert: assert _skill_gate(findings336, pushed_sha=head)["codex_state"] == "polling"
+    assert: assert gated["codex_state"] == "polling" and gated["codex_findings"] == []
+tests/pr_submit/test_codex_reviews.py::test_skill_states_the_a5_rules
+    assert: assert resume.index("pending_retriggers") < resume.index("before the S5 poll")
+    assert: assert fragment in text, fragment
+    assert: assert f"`{name}`" in events, name
+tests/pr_submit/test_conflict_scripts.py::_run_evidence_without_timeout
+    assert: assert not (repos.work / ".git" / "sc-pr-submit-tmp").exists()
+    assert: assert len(res.stdout.splitlines()) == 1, res.stdout
+    assert: assert "\nLIMIT_SECONDS=60\n" in text, "the shipped budget is no longer 60s"
+tests/pr_submit/test_conflict_scripts.py::test_evidence_script_static_rules
+    assert: assert text.startswith("#!/usr/bin/env bash\n")
+    assert: assert "\nset -u -o pipefail\n" in text
+    assert: assert os.access(EVIDENCE, os.X_OK)
+    assert: assert re.search(pattern, text) is None, pattern
+    assert: assert ls.startswith("100755 "), ls
+    regex: re.search(pattern, text)
+tests/pr_submit/test_conflict_scripts.py::test_finish_script_static_rules
+    assert: assert text.startswith("#!/usr/bin/env bash\n")
+    assert: assert "\nset -u -o pipefail\n" in text
+    assert: assert os.access(FINISH, os.X_OK)
+    assert: assert len(re.findall(r"\bgit\s+commit\b", text)) == 1
+    assert: assert len(re.findall(r"\bgit commit -F \"\$MESSAGE_FILE\"", text)) == 1
+    assert: assert re.search(pattern, text) is None, pattern
+    assert: assert ls.startswith("100755 "), ls
+    regex: re.findall(r"\bgit\s+commit\b", text)
+    regex: re.findall(r"\bgit commit -F \"\$MESSAGE_FILE\"", text)
+    regex: re.search(pattern, text)
+tests/pr_submit/test_conflict_scripts.py::test_poll_ci_evidence_mode_static_rules
+    assert: assert re.search(r"(?i)force", text) is None
+    assert: assert text.index('if [ "$EVIDENCE_MODE" -eq 1 ]; then') < text.index( "gh pr checks --repo" )
+    regex: re.search(r"(?i)force", text)
+    regex: re.search(r"\bgh\s+api\b", line)
+    assert: assert "repos/${REPO}/" in line, line
+tests/pr_submit/test_conflict_scripts.py::test_probe_script_static_rules
+    assert: assert text.startswith("#!/usr/bin/env bash\n")
+    assert: assert "\nset -u -o pipefail\n" in text
+    assert: assert os.access(PROBE, os.X_OK)
+    assert: assert re.search(pattern, text) is None, pattern
+    assert: assert ls.startswith("100755 "), ls
+    regex: re.search(pattern, text)
+tests/pr_submit/test_conflict_scripts.py::test_without_timeout_a_hung_read_is_stopped_at_the_budget
+    assert: assert "3-second budget" in res.stderr
+    assert: assert elapsed < 18, f"the run took {elapsed:.1f}s; the budget is 3s"
+tests/pr_submit/test_conflict_scripts.py::test_without_timeout_a_normal_run_still_succeeds
+    assert: assert res.returncode == 0, res.stderr
+    assert: assert res.payload["files"] == ALL_EVIDENCE_FILES
+    assert: assert elapsed < 30, f"the run took {elapsed:.1f}s"
+tests/pr_submit/test_conflict_sync_protocol.py::test_allowed_tools_cover_every_program
+    assert: assert programs <= ALLOWED_PROGRAMS, programs - ALLOWED_PROGRAMS
+    assert: assert programs <= granted, programs - granted
+    assert: assert (SKILL_DIR / script).is_file(), script
+    regex: re.findall(r"Bash\((\S+) \*\)", tools_line)
+tests/pr_submit/test_conflict_sync_protocol.py::test_command_summarizes_conflict_protocol_without_replacing_activation
+    assert: assert "## Merge-conflict handling" in text
+    assert: assert "`--conflict-max-tier` (default 0)" in text
+    assert: assert "before the first review" in text
+    assert: assert "at most one conflict cycle per run" in text
+    assert: assert "uncommitted merge in progress" in text
+    assert: assert "no review round" in text
+    assert: assert "not a sandbox" in text
+    assert: assert "Skill sc:pr-submit-protocol" in text
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_pinned_phrases
+    assert: assert phrase in _read(INTENT_REF), phrase
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_intent_record_fields_in_order
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_order_pins
+tests/pr_submit/test_conflict_sync_protocol.py::test_conflict_mechanical_pinned_phrases
+    assert: assert phrase in _read(MECHANICAL_REF), phrase
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_attempt_writes_under_its_own_attempt_directory
+    assert: assert "conflict_attempt(<run-log events>, cycle_id)" in step3
+    assert: assert "cycle_dir := <output-dir>/sync/<cycle_id>/a<attempt>/" in step3
+    assert: assert "sync/<cycle_id>/resolution.md" not in mechanical
+    assert: assert "--out <cycle_dir><n>/" in intent
+    assert: assert "<cycle_dir>resolution.md" in intent
+    assert: assert "`<cycle_dir>` (this attempt only) as `output_dir`" in intent
+    assert: assert "<output-dir>/sync/<cycle_id>/<n>/" not in intent
+tests/pr_submit/test_conflict_sync_protocol.py::test_every_git_push_in_new_files_is_the_one_form
+    assert: assert seen >= 1
+    assert: assert match.group(0).strip() == PUSH_LINE, (path.name, match.group(0))
+tests/pr_submit/test_conflict_sync_protocol.py::test_evidence_script_named_only_in_conflict_intent
+    assert: assert name in _read(INTENT_REF)
+    assert: assert not offenders, offenders
+tests/pr_submit/test_conflict_sync_protocol.py::test_fr21_prohibited_operation_scan
+    assert: assert not hits, "prohibited operations:\n" + "\n".join(hits)
+tests/pr_submit/test_conflict_sync_protocol.py::test_intent_and_validator_lines_say_tier_2
+    assert: assert not offenders, "lines without a Tier 2 label:\n" + "\n".join(offenders)
+    assert: assert old in skill, old
+tests/pr_submit/test_conflict_sync_protocol.py::test_no_src_superclaude_path
+    assert: assert "src/superclaude" not in _read(path)
+tests/pr_submit/test_conflict_sync_protocol.py::test_skill_edit_present
+    assert: assert fragment in text, f"{edit}: missing {fragment!r}"
+tests/pr_submit/test_conflict_sync_protocol.py::test_skill_keeps_one_python_block
+    assert: assert len(fences) == 1
+tests/pr_submit/test_conflict_sync_protocol.py::test_skill_replaced_text_is_gone
+    assert: assert "and rebase if behind `origin/<base>` (with `--pr <N>`" not in text
+    assert: assert "needs a force-push" not in binding
+tests/pr_submit/test_conflict_sync_protocol.py::test_spec_byte_identical_fragments_survive
+    assert: assert "with `--pr <N>`, at any level, do not rebase" in skill
+    assert: assert "rebase if behind `origin/<base>`" in skill
+    assert: assert "push any commit besides the cycle's one fix commit" in _read(COMMAND_MD)
+    assert: assert "the commit to push must have exactly one parent, that same SHA" in machine
+    assert: assert "The parent check applies only when the cycle applied edits" in machine
+    assert: assert fragment in wave6, fragment
+tests/pr_submit/test_conflict_sync_protocol.py::test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock
+    assert: assert ( "<python> -I -c 'import json, sys; from superclaude.pr_submit.conflicts" in step5 )
+    assert: assert "`uv run --no-sync python`" in step5
+    assert: assert "never use plain `uv run`" in step5
+tests/pr_submit/test_conflict_sync_protocol.py::test_trust_limit_is_documented_in_the_refs_skill_and_command
+    assert: assert "collaborators you trust with your credentials" in _prose(path), path
+tests/pr_submit/test_cosmos_protocol.py::attended_gate
+    assert: assert len(blocks) == 1, "keep one executable snapshot gate, not parallel parsers"
+    regex: re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context
+    assert: assert core.classify is classifier.classify
+    assert: assert core.actionable_finding_comments is classifier.actionable_finding_comments
+    assert: assert core.finding_from_comment is severity_router.finding_from_comment
+    assert: assert gated["review_state"] == "findings"
+    assert: assert classification == selection
+    assert: assert classification.args[0] is payload
+    assert: assert classification.kwargs == { "watermark": WATERMARK, "current_head_sha": HEAD, }
+    assert: assert (finding.comment_id, finding.thread_id, finding.review_id) == ( 4296483537, "PRRT_pr266_example", 5550158176, )
+    assert: assert finding.line is None and finding.original_line == 172
+    assert: assert finding.is_outdated and finding.verification_status == "unverified"
+    assert: assert not is_groundable(finding)
+    assert: assert gated["routes"] == ["report-only"]
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override
+    assert: assert core.classify(payload, contract, current_head_sha=HEAD) == ( "clean" if resolved else "findings" )
+    assert: assert gated["review_state"] == "polling"
+    assert: assert gated["findings"] == gated["routes"] == []
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean
+    assert: assert core.classify(payload, contract, watermark=WATERMARK) == "findings"
+    assert: assert ( core.actionable_finding_comments(payload, contract, watermark=WATERMARK) == [] )
+    assert: assert gated["review_state"] == "polling"
+    assert: assert gated["findings"] == gated["routes"] == []
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_incomplete_sources_do_not_normalize
+    assert: assert gated["review_state"] == "polling"
+    assert: assert gated["findings"] == gated["routes"] == []
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_normalization_valueerror_discards_entire_batch
+    assert: assert len(selected) == 2
+    assert: assert gated["review_state"] == "polling"
+    assert: assert gated["findings"] == gated["routes"] == []
+tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution
+    assert: assert gated["review_state"] == ("clean" if watermark == WATERMARK else "polling")
+    assert: assert gated["findings"] == []
+tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates
+    assert: assert (contract.augment_bot_login, contract.augment_app_slug) == ( "augmentcode[bot]", "augmentcode", )
+    assert: assert contract.accepted_trigger_phrases[0] == "auggie review"
+    assert: assert fragment in text, (name, fragment)
+tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root
+    assert: assert result.returncode == 0, result.stderr
+    assert: assert core.poll_succeeded(payload)
+    assert: assert any("endCursor=c1" in call for call in calls)
+    assert: assert any("page=2" in call for call in calls)
+    assert: assert gated["review_state"] == "findings"
+    assert: assert len(gated["findings"]) == 1
+    assert: assert (finding.comment_id, finding.thread_id, finding.review_id) == ( 4296483537, "PRRT_pr266_example", 5550158176, )
+    assert: assert finding.line is None and finding.original_line == 172
+    assert: assert finding.verification_status == "unverified"
+    assert: assert finding.remapped_severity is core.Severity.LOW
+    assert: assert gated["routes"] == ["report-only"]
+tests/pr_submit/test_static_grep.py::test_poll_script_fetches_issue_and_inline_comments_without_pr_view_comments
+    assert: assert 'gh api "repos/${REPO}/issues/${PR}/comments"' in script
+    assert: assert 'gh api "repos/${REPO}/pulls/${PR}/comments"' in script
+    assert: assert pr_view_lines
+    assert: assert all("comments" not in line for line in pr_view_lines)
+    assert: assert "($issue_comments[0] // []) + ($inline_comments[0] // [])" in script
+    assert: assert "(.comments // [])" not in script
+    assert: assert "--slurpfile issue_comments" in script
+    assert: assert "--slurpfile inline_comments" in script
+    assert: assert "--argjson issue_comments" not in script
+    assert: assert "--argjson inline_comments" not in script
+tests/pr_submit/test_static_grep.py::test_repo_resolution_prefers_origin_over_gh_default
+    assert: assert origin_at < gh_view_at, ( f"{script.name}: `gh repo view` is tried before the origin remote" )
+tests/pr_submit/test_static_grep.py::test_repo_resolution_runs_origin_first_then_falls_back
+    assert: assert with_origin == "acme/widgets", f"{script.name}: got {with_origin!r}"
+    assert: assert no_origin == "upstream/parent", f"{script.name}: got {no_origin!r}"
+tests/pr_submit/test_static_grep.py::test_repo_resolution_sed_handles_all_url_forms
+    regex: re.compile(r"sed -E '([^']*)'")
+    assert: assert script.exists(), f"resolution script missing: {script}"
+    assert: assert match, f"no `sed -E '…'` origin-URL resolution found in {script.name}"
+    assert: assert got == expected, ( f"{script.name}: sed resolved {url!r} → {got!r}, expected {expected!r}" )
+tests/pr_submit/test_static_grep.py::test_s5a_retrigger_widened_for_merge_cycles_only
+    assert: assert ( "or is a Tier 2 merge cycle (push kind `merge`; " "`superclaude.pr_submit.fsm.should_retrigger`)" ) in wave6
+    assert: assert ( "AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) " "or is a Tier 2 merge cycle (push kind `merge`; " "`superclaude.pr_submit.fsm.should_retrigger`), post" ) in wave6
+    assert: assert ( "Next, when the cycle applied edits (a zero-edit cycle has no fix commit" in wave6 )
+    assert: assert "The parent check applies only when the cycle applied edits" in machine
+tests/pr_submit/test_static_grep.py::test_skill_binds_checkout_and_push_target_to_pr_head
+    assert: assert ( "At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and " "return, byte-for-byte identical to today (AC-1)." ) in text
+    assert: assert "with `--pr <N>`, at any level, do not rebase" in text
+    assert: assert "rebase if behind `origin/<base>`" in text
+    assert: assert "rebase if behind `origin/<base>` only at L0" in text
+    assert: assert "Being behind the base branch is not a STOP at L1+" in text
+    assert: assert "branch (`origin/<default-branch>`) on the create path" not in text
+    assert: assert "| Wrong origin / wrong-owner URL |" in text
+    assert: assert "| Behind base branch (create path at L1+, or `--pr`) |" in text
+    assert: assert "reason `pr_head_mismatch`; nothing pushed; do NOT close the PR" in text
+    assert: assert guard < wave6.index("The deterministic core DECIDES")
+    assert: assert "pr_head_ok(<local branch>, pre_push_sha," in wave6
+    assert: assert "never local HEAD" in wave6
+    assert: assert "target_branch := HEAD_BRANCH" in wave6
+    assert: assert "then set `pre_push_sha := target_sha`" in wave6
+    assert: assert wave6.index("pr_head_ok(<local branch>, pre_push_sha,") < parent
+    assert: assert parent < wave6.index("The deterministic core DECIDES")
+    assert: assert "`terminal_halted` (reason `push_range_mismatch`)" in wave6
+    assert: assert ( "| The commit to push is not exactly one commit on top of the PR head" in text )
+    assert: assert "after Branch A, the guard's parent check stops the next push" in text
+    assert: assert fix_commit < wave6.index("Pre-push head guard, before `push_decision`")
+    assert: assert "commit all of them as exactly one commit" in wave6
+    assert: assert wave6.index("(reason `pr_head_mismatch`)") < parent
+    assert: assert ( "Next, when the cycle applied edits (a zero-edit cycle has no fix commit" in wave6 )
+    assert: assert ( "An L3 CI push runs the Wave 6 pre-push head guard and push triad with " "`target_branch := HEAD_BRANCH`" ) in wave8
+    assert: assert "runs the guard's parent check (`push_parent_ok`)" in wave8
+    assert: assert "`terminal_halted` (reason `fix_commit_failed`)" in wave6
+    assert: assert "A crash re-drive (Branch B) skips this step" in wave6
+    assert: assert ( "Branch B: skip the Wave 6 fix commit, set `target_sha` from the record" in text )
+    assert: assert "pre-push head guard with the record's `pre_push_sha`" in text
+    assert: assert ( "| The fix touched a file with the operator's own pending changes, the fix " "commit fails, or HEAD does not advance" ) in text
+    assert: assert ( "staging only the files those edits changed (`git add -- <paths>`, " "never `git add -A` or `git add .`" ) in wave6
+    assert: assert "committing with `git commit --only -- <paths>`" in wave6
+    assert: assert ( "Before the cycle's first edit, record the operator's pending files " "(`git status --porcelain=v1 -z --untracked-files=all`" ) in wave4
+    assert: assert ( "Before staging anything (before the `git add` above), if a path to commit " "is in `OPERATOR_PENDING`" ) in wave6
+    assert: assert "The fix touched files that had your own uncommitted changes: <paths>" in ( wave6 )
+    assert: assert "separate them by hand (do not discard the files)" in wave6
+    assert: assert "A halted cycle replies to and resolves no thread." in wave6
+    assert: assert "The fix commit failed (<error>). Nothing was pushed" in wave6
+    assert: assert "Fix the cause, then either commit and push the fix yourself" in wave6
+    assert: assert "make your checkout equal the new PR head, then re-run" in wave6
+    assert: assert "When this cycle made a fix commit, the message adds:" in wave6
+    assert: assert "This cycle's fixes are in local commit <target_sha>" in wave6
+    assert: assert "the fixes are still in your working tree" not in wave6
+    assert: assert "the commit to push must have exactly one parent, that same SHA" in machine
+    assert: assert "The parent check applies only when the cycle applied edits" in machine
+    assert: assert "push any commit besides the cycle's one fix commit" in will_not
+    assert: assert token in binding, f"Wave 0 head binding is missing {token!r}"
+tests/pr_submit/test_static_grep.py::test_skill_forbids_force_push
+    assert: assert "Force-push (`--force`, `--force-with-lease`, or a `+` refspec)" in will_not
+    assert: assert force.search("git push origin <target_sha>:<target_branch>") is None
+    regex: re.compile(r"\bgit push\b[^`\n]*?(\s--force\b|\s-f\b|\s\+\S)")
+    assert: assert force.search(forced), forced
+    assert: assert hit is None, (path, hit and hit.group(0))
+tests/pr_submit/test_static_grep.py::test_skill_pins_inv_s1_silence_rerequest_tokens
+    assert: assert 'check_idempotent("silence_rerequest_invoked"' in skill
+    assert: assert "rerequested=" in skill
+    assert: assert "rerequested_at=" in skill
+tests/pr_submit/test_static_grep.py::test_t105_runtime_repo_pin
+    assert: assert POLL_SCRIPT.exists(), f"poll script missing: {POLL_SCRIPT}"
+    assert: assert "git remote get-url origin" in script_text, ( "poll script does not resolve the target repo (expected `git remote get-url origin`)" )
+    assert: assert pr_lines, "no runtime `gh pr` command found in the poll script"
+    assert: assert api_lines, "no runtime `gh api` command found in the poll script"
+    assert: assert not pr_offenders, ( "runtime `gh pr` lines missing a `--repo <resolved>` pin (bare → upstream-default risk):\n" + "\n".join(pr_offenders) )
+    assert: assert not api_offenders, ( "runtime `gh api` lines not pinned to a repos/<owner/repo>/ path or graphql:\n" + "\n".join(api_offenders) )
+    regex: re.search(r"\bgh\s+pr\b", line)
+    regex: re.search(r"\bgh\s+api\b", line)
+tests/pr_submit/test_static_grep.py::test_t1101_retrigger_gh_is_repo_scoped
+    assert: assert not offenders, "Unscoped gh in re-trigger surfaces:\n" + "\n".join(offenders)
+    assert: assert path.exists(), f"re-trigger surface missing: {path}"
+tests/pr_submit/test_static_grep.py::test_t1105_retrigger_token_in_script_not_core
+    assert: assert "auggie review" in script
+    assert: assert "auggie review" not in fsm_src, "hard-coded trigger literal in fsm.py"
+tests/pr_submit/test_static_grep.py::test_t1115_auggie_fallback_flag_parity
+    assert: assert flag_string in fallback
+    assert: assert flag_string in pr_submit_skill
+    assert: assert "quick" in depth_row, "`quick` is not an accepted value on the --depth row"
+    assert: assert "`prism-b`" in model_row, ( "prism-b is not the documented --auggie-model default" )
+    assert: assert invocation_lines, "no fallback invocation found in fallback docs or skill"
+    assert: assert f"| `{flag}`" in cmd, ( f"fallback flag {flag!r} is not a defined option row in auggie-review.md" )
+    regex: re.findall( r"`(> Skill sc:auggie-review-protocol[^`]*)`", pr_submit_skill )
+    assert: assert "--no-post-pr" not in ln, f"invocation passes --no-post-pr: {ln}"
+    assert: assert "--auggie-model" not in ln, f"invocation passes --auggie-model: {ln}"
+tests/pr_submit/test_static_grep.py::test_tn50_core_pure_no_gh_git_tokens
+    assert: assert not offenders, "gh/git tokens in core-pure files:\n" + "\n".join(offenders)
+    regex: re.compile(r"\bgh\b|\bgit\b")
+    assert: assert path.exists(), f"core-pure file missing: {path}"
+tests/pr_submit/test_static_grep.py::test_wait_only_sentences_name_the_one_sync_exception
+    assert: assert ( "the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a " "wait-only path allows, and it is not a fix" ) in skill
+    assert: assert ( "never an additional fix or fix push. The single exception is the one Tier 1 " "sync push (5.2d), which is not a fix." ) in machine
+    assert: assert ( "the one Tier 1 sync push of Wave 8a is the only push allowed here, and it is " "not a fix" ) in ci_poll
+tests/skills/test_worker_contract.py::_check_all_classified
+    assert: assert not missing, "unclassified git/gh write-verb hits:\n" + "\n".join( f"{p} [{v}] {ln[:120]}" for p, v, ln in missing )
+tests/skills/test_worker_contract.py::_scan_write_verbs
+    regex: re.sub(r"\s+", " ", re.sub(r"\s+-C\s+\S+", "", m))
+    regex: re.sub(r"\s+-C\s+\S+", "", m)
+tests/skills/test_worker_contract.py::test_classification_table_has_no_stale_entries
+    assert: assert not stale, "classified lines no longer present:\n" + "\n".join( f"{p} [{v}] {ln[:120]}" for p, v, ln in stale )
+tests/skills/test_worker_contract.py::test_each_classification_has_one_category_and_a_reason
+    assert: assert _CATEGORY_RE.match(category), f"bad category {category!r}"
+    assert: assert reason.strip() and "\n" not in reason, "each hit needs a one-line reason"
+tests/skills/test_worker_contract.py::test_every_write_verb_hit_is_classified
+
+## Footer
+scanned test files:
+  tests/commands/test_impact_command.py
+  tests/core/test_how_we_work_routing_table.py
+  tests/pr_submit/__init__.py
+  tests/pr_submit/conftest.py
+  tests/pr_submit/test_auggie_fallback.py
+  tests/pr_submit/test_augment_review_remediation.py
+  tests/pr_submit/test_autonomy_gates.py
+  tests/pr_submit/test_ci_classify.py
+  tests/pr_submit/test_codex_reviews.py
+  tests/pr_submit/test_conflict_e2e.py
+  tests/pr_submit/test_conflict_scripts.py
+  tests/pr_submit/test_conflict_sync_protocol.py
+  tests/pr_submit/test_conflicts_core.py
+  tests/pr_submit/test_contract_setup_diagnosis.py
+  tests/pr_submit/test_contract_setup_evidence.py
+  tests/pr_submit/test_contract_setup_pr_submit_integration.py
+  tests/pr_submit/test_contract_setup_questions.py
+  tests/pr_submit/test_contract_setup_validation.py
+  tests/pr_submit/test_contract_setup_writer.py
+  tests/pr_submit/test_cosmos_poll.py
+  tests/pr_submit/test_cosmos_protocol.py
+  tests/pr_submit/test_cosmos_review.py
+  tests/pr_submit/test_crash_recovery.py
+  tests/pr_submit/test_detection_contract.py
+  tests/pr_submit/test_edge_cases.py
+  tests/pr_submit/test_finding_verify.py
+  tests/pr_submit/test_gate_helper_coverage.py
+  tests/pr_submit/test_gate_helper_differentials.py
+  tests/pr_submit/test_idempotency.py
+  tests/pr_submit/test_loop_guard.py
+  tests/pr_submit/test_monitor_arm.py
+  tests/pr_submit/test_pre_pr_checks.py
+  tests/pr_submit/test_rate_limit.py
+  tests/pr_submit/test_reply_resolve.py
+  tests/pr_submit/test_review_retrigger.py
+  tests/pr_submit/test_run_log.py
+  tests/pr_submit/test_setup_questions_resolution.py
+  tests/pr_submit/test_severity_router.py
+  tests/pr_submit/test_silence.py
+  tests/pr_submit/test_skill_parse.py
+  tests/pr_submit/test_static_grep.py
+  tests/pr_submit/test_timeout.py
+  tests/pr_submit/test_troubleshoot_seed.py
+  tests/pr_submit/test_validated_not_verified.py
+  tests/pr_submit/test_validation_gate.py
+  tests/skills/test_worker_contract.py
+  tests/unit/test_cli_install.py
+target files:
+  src/superclaude/commands/pr-submit.md
+  src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md
+  src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
+  src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh
+  src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh
+  src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh
+  src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
+  src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
+  src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
+  src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh
+pass A rows: 416
+pass B readers: 59
+command: uv run python -I .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py
+caps: literal display 200 characters, assert and regex source 600 characters; the full text is in the named test
+<!-- o3-scan:end -->
+
+Rules that are not text pins and that the block does not show:
 
 - `tests/skills/test_worker_contract.py`: `WRITE_VERB_RE` matches whole-word `gh pr`, `gh api` and the git write verbs on every line under `src/superclaude/{skills,commands,agents}` (scripts included). Each hit must be a key of `WRITE_VERB_CLASSIFICATION`: (repo-relative path, verb text joined with `+` when a line has several, exact stripped line) with a category (`never-worker` for pr-submit, with the standard reason text) and a one-line reason. `test_every_write_verb_hit_is_classified` fails on an unclassified hit; `test_classification_table_has_no_stale_entries` fails when a classified line no longer exists, so the existing Wave 0, Wave 0 head binding, Wave 0 conflict check, Wave 6 and Wave 8a lines of `SKILL.md` are exact keys and must stay byte-identical; new Wave bullets are new physical lines.
-- `tests/pr_submit/test_static_grep.py`: `CORE_PURE_FILES` (no whole word `gh` or `git` in `refs/state-machine.md`, `refs/severity-routing.md`, `refs/loop-guard.md`, the core modules and, after Task 5, `merge_guard.py`); `test_skill_binds_checkout_and_push_target_to_pr_head` (Wave 0 head-binding slice ends at `\n- **Wave 1`; the Wave 6 slice from `- **Wave 6 (L3 only):**` to `\n- **Wave 6b` holds ordered pinned phrases: head guard before `The deterministic core DECIDES`, `pr_head_ok(<local branch>, pre_push_sha,`, `then set `pre_push_sha := target_sha``, `commit all of them as exactly one commit`, `A crash re-drive (Branch B) skips this step`, the fix-commit-failed and operator-pending messages, `When this cycle made a fix commit, the message adds:`); `test_skill_forbids_force_push` (Will Not text and the push-line form); `test_wait_only_sentences_name_the_one_sync_exception`; `test_s5a_retrigger_widened_for_merge_cycles_only`; the `state-machine.md` sentences ("the commit to push must have exactly one parent, that same SHA", "The parent check applies only when the cycle applied edits").
-- `tests/pr_submit/test_conflict_sync_protocol.py`: `SKILL_EDITS` pins (E1 to E13) with `test_skill_edit_present` and `test_skill_replaced_text_is_gone`; `test_skill_keeps_one_python_block` (exactly one python fence in `SKILL.md`); `test_intent_and_validator_lines_say_tier_2` (a line naming `evidence-validator` or `conflict-intent.md` must also say "Tier 2"; new lines avoid both words); `test_evidence_script_named_only_in_conflict_intent`; `test_gh_command_lines_are_repo_scoped`; `test_no_src_superclaude_path` (no `src/superclaude` text in skill or command files); `test_allowed_tools_cover_every_program`; `test_user_guides_document_conflict_cap_and_limits` and `test_command_summarizes_conflict_protocol_without_replacing_activation` (the command file keeps its Activation section and the conflict summary).
-- `tests/pr_submit/test_codex_reviews.py`: `test_skill_states_the_a5_rules` pins these exact `SKILL.md` fragments: `dedup_groups(findings)`, `routes at its members' highest remapped tier`, ``fix_applied` is recorded for **every** member's `fix_key``, `**every verified member's thread** is replied to and resolved`, `"flagged by: augment, codex"`, `covers **only the reviewers re-triggered in this cycle**`, a line break between `at least one` and `re-triggered reviewer reaches `done``, `reviewer_incomplete{reviewer, phase: "rereview"}`, ``plus any merged Codex `findings``, `rebuild_state()["absent_reviewers"]`, `pending_retriggers(`, `rereview_requested{cycle_id, reviewer, timestamp}`, ``reuse the `cycle_id` of the dangling push record``; it also checks that the text from `Every event that concerns one reviewer` to `On `--resume`` names the events `poll_result`, `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`, `route_decision`, `reply_posted`, `thread_resolved` and `rereview_requested`, and that in the `**Resume of a re-triggered cycle:**` text `pending_retriggers` comes before `before the S5 poll`. The same file holds the `len(EventType)` pin (Task 2) and `_skill_gate`, which executes the single python fence of `SKILL.md`.
-- `tests/pr_submit/test_cosmos_protocol.py`: `test_protocol_refs_pin_live_boundaries_and_existing_gates` pins, in `SKILL.md`: `RunConfig.rereview_outcome`, `optimistic legacy default`, `evidence-validator`, a line break inside `without` / `resetting elapsed time`, ``Never pass `review_state="findings"` with an empty `findings` list``; in `refs/detection-contract.md`: `not a stable` / `public API`, `documentary fields, not runtime parser rules`, `lower bound`, `strictly` / `newer than `watermark``, `observed_at`; in `refs/augment-poll.md`: `reviews_ok`, `comments_ok`, `threads_ok`, `comments(first:1)`, `pageInfo{hasNextPage endCursor}`, `all three flags false`; in `refs/review-retrigger.md`: `body="auggie review"`, `payload.head_sha == pushed_sha`, `RunConfig.rereview_outcome`, `strictly newer`, `observed_at`; in `refs/severity-routing.md`: `finding_from_comment(raw)`, `ValueError`, `LF or CRLF`, `verification_status="unverified"`, `evidence-validator`; in `refs/thread-reply.md`: `--thread-id`, `no path/line lookalike match`, `idempotency_skip BEFORE reply`, `hasNextPage:false`, `thread.isResolved:true`. It also loads the shipped detection contract (`augmentcode[bot]`, `augmentcode`, first trigger phrase `auggie review`). It carries the one-python-fence rule too (`_skill_gate`).
-- `tests/pr_submit/test_conflict_sync_protocol.py`: `test_spec_byte_identical_fragments_survive` pins, in `SKILL.md`: `with `--pr <N>`, at any level, do not rebase`, `rebase if behind `origin/<base>``, and inside the Wave 6 slice `pr_head_ok(<local branch>, pre_push_sha,`, `push_parent_ok(<parents>, pre_push_sha)`, `The deterministic core DECIDES`, `then set `pre_push_sha := target_sha``; in `commands/pr-submit.md`: `push any commit besides the cycle's one fix commit`; in `refs/state-machine.md`: the two parent-check sentences named above.
-- Other readers of the pr-submit files, satisfied by additive edits that leave existing text unchanged: `tests/pr_submit/test_edge_cases.py` (`test_ec16_base_branch_halt_documented`: `SKILL.md` keeps `Wrong origin`, `behind` or `wrong-owner`; the poll script keeps `command -v gh`), `tests/commands/test_impact_command.py` (the `sc-pr-submit-protocol/SKILL.md` and `refs/troubleshoot-dispatch.md` impact-skill invocation lines), `tests/core/test_how_we_work_routing_table.py` (routing rows that name `sc:pr-submit`; it reads no pr-submit protocol text), `tests/pr_submit/test_conflict_scripts.py` and `test_cosmos_poll.py` (script behaviour, not text). `test_silence.py`, `test_pre_pr_checks.py` and `test_conflict_e2e.py` read the core modules, not the protocol text.
-- `tests/pr_submit/test_run_log.py`: `_NEW_KEY_DEFAULTS` exact key-set pin (Task 5); the event-count test (Task 2).
-- `src/superclaude/commands/pr-submit.md`: front matter `argument-hint`, `## Options`, `## Merge-conflict handling`, `## Activation` stay; additive edits only.
 - `ruff format --check` formats python fences inside Markdown under `src/`: the new `refs/merge-guard.md` carries no python fence (the pure-module names appear as plain text).
 
 ### O4 S5a and Wave 6 pre-push text

diff --git a/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py b/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py
new file mode 100644
index 00000000..fd2553bd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py
@@ -0,0 +1,285 @@
+"""Read-only inventory of the tests that pin the pr-submit protocol text (plan task 1, O3).
+
+Prints, to stdout, every exact-text pin and every absence or line rule that a test
+holds on the pr-submit skill folder or the pr-submit command file. Standard library
+only; reads files, writes nothing, makes no network call. Run from the repo root:
+
+    uv run python <this file>
+
+A READER is a test function or helper that reads target text: it calls a read function
+(read_text, _read, _prose, ...) on something that names a target file (a target token or
+a module constant that, directly or through other constants, holds one), or loops over
+such constants and reads the loop variable, or calls a helper that does. Tests that scan
+whole folders through a constant that holds no target token are listed in FORCED_READERS
+with the reason.
+
+Pass A: every string literal of 8 or more characters, held by a reader or by a module
+constant a reader uses, that appears verbatim in a target file (raw text or prose form)
+and is not just a path.
+Pass B: every reader, with the source of each assert and each regular-expression call.
+"""
+
+from __future__ import annotations
+
+import ast
+import re
+import sys
+from pathlib import Path
+
+REPO = Path(__file__).resolve().parents[5]
+SKILL_REL = "src/superclaude/skills/sc-pr-submit-protocol"
+COMMAND_REL = "src/superclaude/commands/pr-submit.md"
+TOKENS = (
+    "sc-pr-submit-protocol",
+    "pr-submit.md",
+    "state-machine.md",
+    "loop-guard.md",
+    "ci-poll.md",
+    "review-retrigger.md",
+)
+EXTRA_TESTS = (
+    "tests/skills/test_worker_contract.py",
+    "tests/commands/test_impact_command.py",
+    "tests/core/test_how_we_work_routing_table.py",
+)
+# Readers the token rule cannot see: the write-verb audit scans every file under the skills,
+# commands and agents folders (AUDIT_ROOTS), which includes the pr-submit files.
+FORCED_READERS = {
+    "tests/skills/test_worker_contract.py": (
+        "test_every_write_verb_hit_is_classified",
+        "test_classification_table_has_no_stale_entries",
+        "test_each_classification_has_one_category_and_a_reason",
+        "_check_all_classified",
+        "_scan_write_verbs",
+    )
+}
+READ_CALLS = {"read_text", "_read", "_prose", "_text", "read_bytes"}
+LITERAL_CAP = 200
+SOURCE_CAP = 600
+PATHLIKE = re.compile(
+    r"^[\w./*\[\]-]+\.(md|sh|py|yaml|yml|json|jsonl|toml)$|^(src|tests|docs|\.dev)/[\w./*-]*$"
+)
+
+
+def targets() -> dict[str, tuple[str, str]]:
+    found = {}
+    files = [REPO / COMMAND_REL] + sorted(
+        p for p in (REPO / SKILL_REL).rglob("*") if p.is_file() and p.suffix in (".md", ".sh")
+    )
+    for path in files:
+        raw = path.read_text(encoding="utf-8")
+        prose = " ".join(raw.replace("\n> ", " ").split())
+        found[str(path.relative_to(REPO))] = (raw, prose)
+    return found
+
+
+def scanned_tests() -> list[Path]:
+    chosen = set((REPO / "tests/pr_submit").glob("*.py"))
+    chosen.update(REPO / rel for rel in EXTRA_TESTS)
+    for path in (REPO / "tests").rglob("*.py"):
+        text = path.read_text(encoding="utf-8", errors="replace")
+        if "sc-pr-submit-protocol" in text or "pr-submit" in text:
+            chosen.add(path)
+    return sorted(p for p in chosen if p.exists())
+
+
+def segment(source: str, node: ast.AST) -> str:
+    return ast.get_source_segment(source, node) or ""
+
+
+def short(text: str, cap: int) -> str:
+    text = " ".join(text.split())
+    return text if len(text) <= cap else text[:cap] + f" [+{len(text) - cap} chars]"
+
+
+class Analysis:
+    """Readers and the module constants they use, for one test file."""
+
+    def __init__(self, path: Path) -> None:
+        self.path = path
+        self.source = path.read_text(encoding="utf-8", errors="replace")
+        self.tree = ast.parse(self.source)
+        self.values: dict[str, ast.AST] = {}
+        self.funcs: dict[str, ast.AST] = {}
+        for node in self.tree.body:
+            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
+                self.funcs[node.name] = node
+            elif isinstance(node, ast.Assign):
+                for target in node.targets:
+                    if isinstance(target, ast.Name):
+                        self.values[target.id] = node.value
+            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value:
+                self.values[node.target.id] = node.value
+        self.target_names = self._target_names()
+        rel = str(path.relative_to(REPO))
+        forced = set(FORCED_READERS.get(rel, ()))
+        self.readers = {n for n, fn in self.funcs.items() if n in forced or self._reads_target(fn, 0)}
+        self.used_constants = self._used_constants()
+
+    def _target_names(self) -> set[str]:
+        hit = {n for n, v in self.values.items() if any(t in segment(self.source, v) for t in TOKENS)}
+        changed = True
+        while changed:
+            changed = False
+            for name, value in self.values.items():
+                if name in hit:
+                    continue
+                if any(isinstance(s, ast.Name) and s.id in hit for s in ast.walk(value)):
+                    hit.add(name)
+                    changed = True
+        return hit
+
+    def _mentions(self, node: ast.AST, extra: set[str]) -> bool:
+        if any(t in segment(self.source, node) for t in TOKENS):
+            return True
+        return any(isinstance(s, ast.Name) and (s.id in self.target_names or s.id in extra) for s in ast.walk(node))
+
+    def _reads_target(self, fn: ast.AST, depth: int) -> bool:
+        loop_vars: set[str] = set()
+        # a parametrized test whose decorator names a target file reads through its parameters
+        if any(self._mentions(d, set()) for d in getattr(fn, "decorator_list", [])):
+            loop_vars.update(a.arg for a in fn.args.args)
+        for sub in ast.walk(fn):
+            if isinstance(sub, ast.For) and self._mentions(sub.iter, set()):
+                loop_vars.update(n.id for n in ast.walk(sub.target) if isinstance(n, ast.Name))
+        for sub in ast.walk(fn):
+            if not isinstance(sub, ast.Call):
+                continue
+            func = sub.func
+            if isinstance(func, ast.Attribute) and func.attr in READ_CALLS:
+                if self._mentions(func.value, loop_vars):
+                    return True
+            elif isinstance(func, ast.Name) and func.id in READ_CALLS:
+                if sub.args and self._mentions(sub.args[0], loop_vars):
+                    return True
+            elif isinstance(func, ast.Name) and func.id in self.funcs and depth < 3:
+                if self._mentions(sub, loop_vars) or self._reads_target(self.funcs[func.id], depth + 1):
+                    return True
+        return False
+
+    def _used_constants(self) -> set[str]:
+        used: set[str] = set()
+        frontier = [self.funcs[n] for n in self.readers]
+        while frontier:
+            node = frontier.pop()
+            for sub in ast.walk(node):
+                if isinstance(sub, ast.Name) and sub.id in self.values and sub.id not in used:
+                    used.add(sub.id)
+                    frontier.append(self.values[sub.id])
+        return used
+
+
+def owner_map(tree: ast.Module) -> dict[int, tuple[str, str]]:
+    """id(node) -> (base owner name, display label)."""
+    out: dict[int, tuple[str, str]] = {}
+
+    def mark(node: ast.AST, base: str, label: str) -> None:
+        for sub in ast.walk(node):
+            out[id(sub)] = (base, label)
+
+    for node in tree.body:
+        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
+            mark(node, node.name, node.name)
+        elif isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None:
+            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
+            name = next((t.id for t in targets if isinstance(t, ast.Name)), "<module>")
+            if isinstance(node.value, ast.Dict):
+                for key, value in zip(node.value.keys, node.value.values):
+                    label = f"{name}[{short(ast.unparse(key), 70)}]" if key is not None else name
+                    mark(value, name, label)
+            else:
+                mark(node.value, name, name)
+    return out
+
+
+def how_checked(parents: dict[int, ast.AST], node: ast.AST) -> str:
+    parent = parents.get(id(node))
+    if isinstance(parent, ast.Compare):
+        return "not in" if any(isinstance(op, ast.NotIn) for op in parent.ops) else (
+            "in" if any(isinstance(op, ast.In) for op in parent.ops) else "compare"
+        )
+    if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Attribute):
+        return f".{parent.func.attr}()"
+    if isinstance(parent, (ast.Tuple, ast.List, ast.Set, ast.Dict)):
+        return "set member"
+    return "other"
+
+
+def pass_a(analyses: list[Analysis], found: dict[str, tuple[str, str]]) -> list[str]:
+    rows = []
+    for an in analyses:
+        owners = owner_map(an.tree)
+        parents = {id(c): n for n in ast.walk(an.tree) for c in ast.iter_child_nodes(n)}
+        seen = set()
+        for node in ast.walk(an.tree):
+            if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
+                continue
+            base, label = owners.get(id(node), ("<module>", "<module>"))
+            if base not in an.readers and base not in an.used_constants:
+                continue
+            text = node.value
+            if len(text) < 8 or PATHLIKE.match(text.strip()):
+                continue
+            hit_files = [rel for rel, (raw, prose) in found.items() if text in raw or text in prose]
+            if not hit_files:
+                continue
+            row = (
+                f"{an.path.relative_to(REPO)}::{label} | {', '.join(hit_files)} | "
+                f"{how_checked(parents, node)} | {short(text.replace(chr(10), chr(92) + 'n'), LITERAL_CAP)}"
+            )
+            if row not in seen:
+                seen.add(row)
+                rows.append(row)
+    return rows
+
+
+def pass_b(analyses: list[Analysis]) -> list[str]:
+    rows = []
+    for an in analyses:
+        for name in sorted(an.readers):
+            fn = an.funcs[name]
+            rows.append(f"{an.path.relative_to(REPO)}::{name}")
+            for sub in ast.walk(fn):
+                if isinstance(sub, ast.Assert):
+                    rows.append("    assert: " + short(segment(an.source, sub), SOURCE_CAP))
+                elif (
+                    isinstance(sub, ast.Call)
+                    and isinstance(sub.func, ast.Attribute)
+                    and isinstance(sub.func.value, ast.Name)
+                    and sub.func.value.id == "re"
+                    and sub.func.attr in {"compile", "search", "match", "findall", "sub", "fullmatch"}
+                ):
+                    rows.append("    regex: " + short(segment(an.source, sub), SOURCE_CAP))
+    return rows
+
+
+def main() -> int:
+    found = targets()
+    analyses = [Analysis(p) for p in scanned_tests()]
+    a_rows = pass_a(analyses, found)
+    b_rows = pass_b(analyses)
+    readers = sum(len(an.readers) for an in analyses)
+    print("## Pass A: exact-text pins (test::owner | target file | how checked | literal)")
+    print("\n".join(a_rows))
+    print()
+    print("## Pass B: readers of target text (test or helper), with their asserts and regex calls")
+    print("\n".join(b_rows))
+    print()
+    print("## Footer")
+    print("scanned test files:")
+    print("\n".join(f"  {an.path.relative_to(REPO)}" for an in analyses))
+    print("target files:")
+    print("\n".join(f"  {rel}" for rel in found))
+    print(f"pass A rows: {len(a_rows)}")
+    print(f"pass B readers: {readers}")
+    here = Path(__file__).resolve().relative_to(REPO)
+    print(f"command: uv run python -I {here}")
+    print(
+        f"caps: literal display {LITERAL_CAP} characters, assert and regex source {SOURCE_CAP} "
+        "characters; the full text is in the named test"
+    )
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
Earlier blocking findings of this start (empty on the first review): F2.1 sev=blocking trigger=B1 ac=T1.AC3 at=.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md:50-65 anchor="lists every exact-text pin and line-content rule found for O3" chk=y,n,n,n family=o3-pin-completeness fix=In O3, add the exact text and files of the `test_wait_only_sentences_name_the_one_sync_exception` sentences (they sit in SKILL.md, `refs/state-machine.md` and `refs/ci-poll.md`, not only the state-machine). Add the `test_skill_forbids_force_push` rule: no `git push` followed on the same line by `--force`, `-f` or a `+` refspec in any .md or .sh under the skill directory, plus the exact Will Not Do sentence. Add `test_skill_pins_inv_s1_silence_rerequest_tokens` (SKILL.md must keep `check_idempotent("silence_rerequest_invoked"`, `rerequested=` and `rerequested_at=`). Add `test_t1115_auggie_fallback_flag_parity` (SKILL.md must keep the string `--depth quick --remediation-offer`). Add `test_t1101_retrigger_gh_is_repo_scoped` (every `gh` line in `refs/review-retrigger.md` and `retrigger-review.sh` must be repo-scoped). covers="lists every exact-text pin and line-content rule found for O3" first=A1 origin=late: the added pin lists cover three tests; several others are named by test name only or not at all (wait-only sentences, force-push rule, silence-token pins at tests/pr_submit/test_static_grep.py:243-248, the `--depth quick --remediation-offer` pin at :273-277, the re-trigger repo-scope rule at :224-240, and the 13 SKILL_EDITS pin texts E1 to E13 by symbol only).
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
