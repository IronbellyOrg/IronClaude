fdb08e60c8c3f45bcd1681cd1c79c40da4247b65
Review one task for spec compliance.

Task brief: ## Task 1: Add the alias-only policy tests

Create tests/skills/test_model_alias_policy.py (ROOT = Path(__file__).resolve().parents[2], like tests/skills/test_issue_worker_agents.py, which also shows how agent frontmatter is parsed). Define ALIASES = opus, sonnet, haiku, inherit and two allow-list constants, each with a one-line reason: ISSUE_WORKER_PINS (the three issue-worker agent files, whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a; reason: they stop with E-TIER-UNAVAILABLE outside a ccsession tier workspace, see src/superclaude/skills/sc-issue-protocol/refs/tiers.md) and TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here). Tests, each with a docstring naming the rule:

- When a `model:` line is present in the frontmatter of a file in src/superclaude/agents/*.md, src/superclaude/skills/*/SKILL.md or src/superclaude/commands/*.md, its value is in ALIASES, except the allow-listed issue workers; files without a `model:` line are skipped.
- The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths.
- No non-docstring string constant in any src/superclaude/**/*.py module, skipping src/superclaude/skills/ccsession-tag/, matches `^claude-(opus|sonnet|haiku|fable)-\d` (parse with ast; comments and docstrings are skipped). A residual allow-list dict (path to reason) exists for any legitimate hit found when the test first runs.
- No line of any .md file under src/superclaude/agents, commands or skills (skipping src/superclaude/skills/ccsession-tag/) passes a full model id to a model flag, matched by `--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-\d`.
- superclaude.cli.reflect.commands._DEFAULT_MODEL is in ALIASES.
- docs/testing/v5.0.0/user/D12-reflect.md does not contain claude-opus-4-8.
- The brainstorm steps in src/superclaude/skills/sc-issue-protocol/refs/chains.md contain no `--models` flag.
- src/superclaude/agents/audit-scanner.md pins `model: sonnet`, and no .md file under src/superclaude/skills/sc-cleanup-audit-protocol/ (SKILL.md and templates/) nor src/superclaude/commands/cleanup-audit.md contains the word Haiku.
- Neither src/superclaude/skills/sc-implement-protocol/refs/retry.md nor refs/ledger.md, nor their copies under plugins/superclaude/skills/sc-implement-protocol/refs/, contains a name matching `T[0-4]_Model`, and retry.md names the primary-ladder variables T3Model01, T2Model02, T1Model02 and T1Model01.
- docs/reference/model-aliases.md exists and states the three exports with the exact ids ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2; and tier1a, tier1b and tier2 are keys of "tiers" in src/superclaude/skills/ccsession-tag/ccsession-models.json (read only).

Acceptance criteria:
- tests/skills/test_model_alias_policy.py exists and `uv run pytest tests/skills/test_model_alias_policy.py` run on the unchanged tree fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test, the cleanup-audit test, the retry names test and the mapping document test; the remaining tests pass. The pytest output is saved to ./artifacts/t1-red.log.
- Every failing test fails for the stated reason (for example the Python constants test reports src/superclaude/cli/reflect/commands.py and claude-opus-4-8), not an import or collection error.
- `uv run ruff check tests/skills/test_model_alias_policy.py` and `uv run ruff format --check tests/skills/test_model_alias_policy.py` pass.

Acceptance criteria ids:
T1.AC1: tests/skills/test_model_alias_policy.py exists and `uv run pytest tests/skills/test_model_alias_policy.py` run on the unchanged tree fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test, the cleanup-audit test, the retry names test and the mapping document test; the remaining tests pass. The pytest output is saved to ./artifacts/t1-red.log.
T1.AC2: Every failing test fails for the stated reason (for example the Python constants test reports src/superclaude/cli/reflect/commands.py and claude-opus-4-8), not an import or collection error.
T1.AC3: `uv run ruff check tests/skills/test_model_alias_policy.py` and `uv run ruff format --check tests/skills/test_model_alias_policy.py` pass.
Global constraints: 
- Do not edit anything under src/superclaude/skills/ccsession-tag/ or any ccsession-orca file (issue #315 owns them); read them only. Do not edit the ccsession launcher in this change.
- Agent, command and skill text keeps the plain aliases opus, sonnet and haiku. The three issue-worker agents (src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md) keep their pinned claude-gw-tier ids as documented allow-list exceptions.
- Edit under src/ only; the .claude/ copies are gitignored sync output regenerated by make sync-dev. Where an edited src/superclaude file has a byte-identical copy under plugins/superclaude/, copy the edited file over that mirror so both stay identical.
- Do not change `model:` values in any agent file, and do not add agent files.
- New text that describes the mapping says it holds once the launcher sets the three variables; today the workspace defaults file exports real model ids for them.
- New files and edits never spell the retired underscore names of the retry-ladder variables literally (build any pattern from a regex such as T[0-4]_Model), so the Task 5 grep stays clean.
- Python commands run through uv (uv run pytest ...). Run only the tests named in a task plus the tests that read the files it edits; never the whole suite and never tests/cli/eval/ as a directory.
- Task-owned evidence is written under ./artifacts/ in this package.
Start sha: fdb08e60c8c3f45bcd1681cd1c79c40da4247b65
Diff against the start snapshot: diff --git a/tests/skills/test_model_alias_policy.py b/tests/skills/test_model_alias_policy.py
new file mode 100644
index 00000000..5d8c31b2
--- /dev/null
+++ b/tests/skills/test_model_alias_policy.py
@@ -0,0 +1,247 @@
+"""Alias-only model selection policy (issue #384, owner decision: option A).
+
+These tests check, at the points each test names, that the agent, command and
+skill files and the Python package under ``src/superclaude`` use the plain aliases
+``opus``, ``sonnet`` and ``haiku`` (or ``inherit`` in frontmatter), apart from the
+allow-lists below. In tier mode the launcher sets each ``ANTHROPIC_DEFAULT_*_MODEL``
+for a tier the owner may use, so those aliases map to tier models inside a
+ccsession tier workspace; otherwise the workspace defaults file's real model ids
+apply. See ``docs/reference/model-aliases.md``.
+
+Enforcement type: STATIC (file text and ast). The allow-lists below are the
+documented exceptions; every entry carries its reason.
+"""
+
+import ast
+import json
+import re
+from pathlib import Path
+
+import pytest
+
+ROOT = Path(__file__).resolve().parents[2]
+SRC = ROOT / "src" / "superclaude"
+ALIASES = {"opus", "sonnet", "haiku", "inherit"}
+
+# Allow-list 1: agents that pin a ccsession picker id on purpose. They stop with
+# E-TIER-UNAVAILABLE outside a ccsession tier workspace (see
+# src/superclaude/skills/sc-issue-protocol/refs/tiers.md).
+ISSUE_WORKER_PINS = {
+    "src/superclaude/agents/issue-worker-t3.md": "claude-gw-tier3",
+    "src/superclaude/agents/issue-worker-t2.md": "claude-gw-tier2",
+    "src/superclaude/agents/issue-worker-t1.md": "claude-gw-tier1a",
+}
+
+# Allow-list 2: paths that may contain the text "claude-gw-tier". The issue
+# workers and their protocol pin tier ids on purpose; ccsession-tag is the
+# launcher package (owned by issue #315, read-only for this policy).
+TIER_TEXT_ALLOWED = (
+    *ISSUE_WORKER_PINS,
+    "src/superclaude/skills/sc-issue-protocol/",
+    "src/superclaude/skills/ccsession-tag/",
+)
+
+# Residual allow-list for full model ids in Python string constants:
+# path -> reason. Empty: the only hit when this test was written was fixed.
+RESIDUAL_FULL_IDS: dict[str, str] = {}
+
+TIER_TEXT_DIRS = ("agents", "commands", "skills", "cli", "hooks", "core")
+TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".sh", ".txt", ".toml"}
+FULL_ID = re.compile(r"^claude-(opus|sonnet|haiku|fable)-\d")
+MODEL_FLAG_WITH_FULL_ID = re.compile(
+    r"--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-\d"
+)
+
+
+def _rel(path: Path) -> str:
+    return path.relative_to(ROOT).as_posix()
+
+
+def _frontmatter_model(path: Path) -> str | None:
+    text = path.read_text(encoding="utf-8")
+    if not text.startswith("---\n"):
+        return None
+    head = text[4:].split("\n---\n", 1)[0]
+    for line in head.splitlines():
+        key, _, value = line.partition(":")
+        if key.strip() == "model":
+            return value.strip().strip("\"'")
+    return None
+
+
+def _markdown_under(*dirs: str) -> list[Path]:
+    found = []
+    for name in dirs:
+        for path in sorted((SRC / name).rglob("*.md")):
+            if "skills/ccsession-tag/" not in path.as_posix():
+                found.append(path)
+    return found
+
+
+def test_frontmatter_model_is_an_alias_when_present() -> None:
+    """A frontmatter ``model:`` is an alias or ``inherit``; issue workers are pinned."""
+    files = [
+        *sorted((SRC / "agents").glob("*.md")),
+        *sorted((SRC / "skills").glob("*/SKILL.md")),
+        *sorted((SRC / "commands").glob("*.md")),
+    ]
+    bad = []
+    for path in files:
+        model = _frontmatter_model(path)
+        if model is None:
+            continue
+        pin = ISSUE_WORKER_PINS.get(_rel(path))
+        if pin is not None:
+            if model != pin:
+                bad.append(f"{_rel(path)}: {model!r} (pinned {pin!r})")
+        elif model not in ALIASES:
+            bad.append(f"{_rel(path)}: {model!r}")
+    assert bad == []
+
+
+def test_tier_ids_appear_only_in_allowed_paths() -> None:
+    """The text ``claude-gw-tier`` stays inside the documented allow-list."""
+    bad = []
+    for name in TIER_TEXT_DIRS:
+        base = SRC / name
+        if not base.is_dir():
+            continue
+        for path in sorted(base.rglob("*")):
+            if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
+                continue
+            rel = _rel(path)
+            if rel.startswith(TIER_TEXT_ALLOWED):
+                continue
+            if "claude-gw-tier" in path.read_text(encoding="utf-8", errors="ignore"):
+                bad.append(rel)
+    assert bad == []
+
+
+def _docstring_ids(tree: ast.AST) -> set[int]:
+    ids = set()
+    for node in ast.walk(tree):
+        if isinstance(
+            node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
+        ):
+            body = node.body
+            if (
+                body
+                and isinstance(body[0], ast.Expr)
+                and isinstance(body[0].value, ast.Constant)
+                and isinstance(body[0].value.value, str)
+            ):
+                ids.add(id(body[0].value))
+    return ids
+
+
+def test_python_selection_constants_are_not_full_model_ids() -> None:
+    """No Python string constant selects a model by a full (dated) model id."""
+    bad = []
+    for path in sorted(SRC.rglob("*.py")):
+        rel = _rel(path)
+        if rel.startswith("src/superclaude/skills/ccsession-tag/"):
+            continue
+        if rel in RESIDUAL_FULL_IDS:
+            continue
+        try:
+            tree = ast.parse(path.read_text(encoding="utf-8"))
+        except SyntaxError:
+            continue
+        docstrings = _docstring_ids(tree)
+        for node in ast.walk(tree):
+            if (
+                isinstance(node, ast.Constant)
+                and isinstance(node.value, str)
+                and id(node) not in docstrings
+                and FULL_ID.match(node.value)
+            ):
+                bad.append(f"{rel}:{node.lineno}: {node.value!r}")
+    assert bad == []
+
+
+def test_markdown_does_not_pass_full_model_ids_to_model_flags() -> None:
+    """No agent, command or skill text hands a full model id to --model/--models."""
+    bad = []
+    for path in _markdown_under("agents", "commands", "skills"):
+        for number, line in enumerate(
+            path.read_text(encoding="utf-8").splitlines(), start=1
+        ):
+            if MODEL_FLAG_WITH_FULL_ID.search(line):
+                bad.append(f"{_rel(path)}:{number}")
+    assert bad == []
+
+
+def test_reflect_default_model_is_an_alias() -> None:
+    """The reflect CLI falls back to the plain alias, not a dated model id."""
+    from superclaude.cli.reflect import commands
+
+    assert commands._DEFAULT_MODEL in ALIASES
+
+
+def test_d12_manual_test_does_not_pin_the_old_reflect_model() -> None:
+    """The D12 validation script expects the alias default, not claude-opus-4-8."""
+    text = (ROOT / "docs/testing/v5.0.0/user/D12-reflect.md").read_text(
+        encoding="utf-8"
+    )
+    assert "claude-opus-4-8" not in text
+
+
+def test_issue_chains_use_the_default_brainstorm_models() -> None:
+    """The /sc:issue chains pass no --models flag to /sc:brainstorm."""
+    text = (SRC / "skills/sc-issue-protocol/refs/chains.md").read_text(encoding="utf-8")
+    steps = re.findall(r"`(/sc:brainstorm[^`]*)`", text)
+    assert len(steps) >= 3
+    assert [step for step in steps if "--models" in step] == []
+
+
+def test_cleanup_audit_docs_match_the_audit_scanner_pin() -> None:
+    """audit-scanner pins sonnet, so the cleanup-audit docs do not say Haiku."""
+    assert _frontmatter_model(SRC / "agents/audit-scanner.md") == "sonnet"
+    files = [
+        *sorted((SRC / "skills/sc-cleanup-audit-protocol").rglob("*.md")),
+        SRC / "commands/cleanup-audit.md",
+    ]
+    assert [_rel(p) for p in files if "Haiku" in p.read_text(encoding="utf-8")] == []
+
+
+RETRY_REFS = (
+    "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
+    "src/superclaude/skills/sc-implement-protocol/refs/ledger.md",
+    "plugins/superclaude/skills/sc-implement-protocol/refs/retry.md",
+    "plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md",
+)
+
+
+def test_retry_ladder_uses_the_variable_names_the_workspace_exports() -> None:
+    """The retry ladder names exported slot variables, not underscore spellings."""
+    retired = re.compile(r"T[0-4]_Model")
+    bad = [
+        rel
+        for rel in RETRY_REFS
+        if retired.search((ROOT / rel).read_text(encoding="utf-8"))
+    ]
+    assert bad == []
+    retry = (ROOT / RETRY_REFS[0]).read_text(encoding="utf-8")
+    for name in ("T3Model01", "T2Model02", "T1Model02", "T1Model01"):
+        assert name in retry
+
+
+def test_mapping_document_states_the_exports_and_tiers_exist() -> None:
+    """The reference page spells the three exports; the tiers are real."""
+    doc = (ROOT / "docs/reference/model-aliases.md").read_text(encoding="utf-8")
+    for line in (
+        "ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a",
+        "ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b",
+        "ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2",
+    ):
+        assert line in doc
+    models = json.loads(
+        (SRC / "skills/ccsession-tag/ccsession-models.json").read_text(encoding="utf-8")
+    )
+    assert {"tier1a", "tier1b", "tier2"} <= set(models["tiers"])
+
+
+@pytest.mark.parametrize("pin", sorted(ISSUE_WORKER_PINS))
+def test_issue_worker_allow_list_entries_exist(pin: str) -> None:
+    """Every allow-listed issue worker file exists (the list cannot go stale)."""
+    assert (ROOT / pin).is_file()
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
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
