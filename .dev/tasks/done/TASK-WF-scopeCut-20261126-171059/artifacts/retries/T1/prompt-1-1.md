5267749cb1f54bbab3b4df6ff0bd24f647b3a39b
Review one task for spec compliance.

Task brief: ## Task 1: Create the script with rendering, branch set and digest

Create `scripts/apply_org_rulesets.py` with a module docstring, the constants `EXIT_OK = 0`, `EXIT_USAGE = 64`, `EXIT_FAILED = 69` (the values at `scripts/worktree_cleanup.py` lines 96 to 98), `ROOT` and `RULES_DIR` (location rule), and the pure functions of source.md section 2.1: `render_branch(branch)`, `render_tags()`, `branch_set(default_branch, existing)`, `plan_bodies(branches)` (the tag body first, then `integration`, then `master`, then any other default branch) and `payload_digest(bodies)` (sha256 of the canonical JSON, sorted keys and fixed separators, of the bodies in that order). Also add `compare_bodies(rendered, remote)` as in section 2.4: it compares `name`, `target`, `enforcement`, `conditions`, `bypass_actors` as a set and `rules` as a set of type plus complete parameters, ignores only the server metadata keys named in one constant, and returns a list of difference descriptions, empty when equal.

Create `tests/org_rulesets/__init__.py`, `tests/org_rulesets/conftest.py` with the session fixture `orr` (loads the script with `importlib.util.spec_from_file_location("apply_org_rulesets", ROOT / "scripts" / "apply_org_rulesets.py")`, registered in `sys.modules`) and `tests/org_rulesets/test_render.py`.

Acceptance criteria:
- `render_branch("master")` and `render_branch("integration")` equal the parsed `protect-master.json` and `protect-integration.json`; `render_tags()` equals the parsed `protect-release-tags.json` and holds the rule types `deletion`, `non_fast_forward` and `update`.
- A branch name that is empty, contains `*` or `~`, or starts with `refs/` raises; no rendered body contains the text `~DEFAULT_BRANCH`.
- `branch_set` returns the expected set for three cases: default `master` only; default `main` with no `integration`; default `integration` with `master` present. It never repeats a name.
- `plan_bodies` returns the order tag, `integration`, `master`, other default branch.
- `payload_digest` is equal for equal input and differs when any body changes or the order changes.
- `compare_bodies` returns an empty list for identical bodies and for a remote body that adds only the ignored metadata keys, and a non-empty list naming the difference for an extra rule, an extra bypass actor, a changed `required_approving_review_count`, a changed `enforcement`, a changed ref and an unknown extra top-level key; rule and bypass-actor order do not matter.
- With the working folder changed to an empty temporary folder, `render_branch` and `render_tags` return the same bodies.
- The closing checks of the Constraints pass.

Global constraints: ## Constraints

- No task calls GitHub or touches any IronbellyGroup repo. Every GitHub call in a test goes through `FakeRunner` of `tests/org_rulesets/conftest.py`; no test starts the real `gh`.
- `.github/rulesets/*.json`, the commands in `docs/developer-guide/branch-protection.md` and `tests/docs/test_branch_protection_rulesets.py` stay unchanged. The only edit to the guide is the one link line of Task 7. The existing test must keep passing.
- Python 3.10, standard library only; ruff rules `E,F,I,N,W,TID` at line length 88 as set in `pyproject.toml`.
- No real private repo name and no real org login is written in any tracked file. Tests use synthetic names such as `acme-one`. The script holds no org or repo name, except the upstream org name it refuses.
- Only these paths may change: `scripts/apply_org_rulesets.py`, `tests/org_rulesets/`, `docs/developer-guide/branch-protection-multi-repo.md`, `docs/developer-guide/branch-protection.md` (one link line) and `docs/developer-guide/documentation-index.md`. Nothing under `.claude/` or `.github/` changes.
- "source.md section 2.3" names a heading of `./source.md`.
- Test setup follows `tests/worktree_cleanup/conftest.py` (the session fixture `wc` at lines 26 to 37 loads the script once; `RecordingRunner` at lines 68 to 109 subclasses the real `Runner` and overrides `_execute`). `tests/org_rulesets/conftest.py` defines the session fixture `orr` (the script module) and every shared fixture exactly once; a test module never imports a fixture from another module, because CI lists fixtures with `pytest --fixtures` and a duplicate crashes it.
- Location rule: the repo root is `Path(__file__).resolve().parent.parent`, the rule files are read from `<root>/.github/rulesets/`, and no function reads the current working folder. The before-state file is written into the folder given with `--out`.
- Choices for the owner's review (all are made inside the scope cut and listed in the pull request): one repo per run; the push check excuses no direct push by a named person; the tag ruleset is applied with a printed warning and a manual check of release workflows; rollback is manual.
- Every task ends with the same checks: `uv run pytest tests/org_rulesets/` passes (plus `tests/docs/test_branch_protection_rulesets.py` from Task 6 on), `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing.

Start sha: 5267749cb1f54bbab3b4df6ff0bd24f647b3a39b
Diff against the start snapshot: diff --git a/scripts/apply_org_rulesets.py b/scripts/apply_org_rulesets.py
new file mode 100644
index 000000000..8adc00875
--- /dev/null
+++ b/scripts/apply_org_rulesets.py
@@ -0,0 +1,130 @@
+#!/usr/bin/env python3
+"""Apply the three IronClaude rulesets to ONE repo of an organisation, one repo per run.
+
+The rule files in ``.github/rulesets/`` are the only source of the rules. This script
+renders them for a repo's branches, checks the repo (a dry run that prints what would
+change) and, only with ``--apply --confirm <digest>``, creates the rulesets and reads
+each one back. It never edits or deletes a ruleset and it never posts the issue comment.
+
+This part holds the pure rendering and comparing functions. The command runner, the
+checks and the command line follow in the same file.
+"""
+
+from __future__ import annotations
+
+import hashlib
+import json
+from pathlib import Path
+
+EXIT_OK = 0
+EXIT_USAGE = 64
+EXIT_FAILED = 69
+
+# The repo root is found from this file, never from the current working folder.
+ROOT = Path(__file__).resolve().parent.parent
+RULES_DIR = ROOT / ".github" / "rulesets"
+
+BRANCH_RULES_FILE = "protect-master.json"
+TAG_RULES_FILE = "protect-release-tags.json"
+
+# The branches that get a ruleset first, in write order; any other default branch
+# follows them.
+FIXED_BRANCHES = ("integration", "master")
+
+# Keys GitHub adds to a ruleset it returns. They are not part of the rules and are the
+# only keys ``compare_bodies`` ignores.
+SERVER_KEYS = frozenset(
+    {
+        "id",
+        "source",
+        "source_type",
+        "node_id",
+        "created_at",
+        "updated_at",
+        "current_user_can_bypass",
+        "_links",
+    }
+)
+
+# Keys whose list order does not matter.
+_SET_KEYS = frozenset({"rules", "bypass_actors"})
+
+
+def _load(name: str) -> dict:
+    return json.loads((RULES_DIR / name).read_text(encoding="utf-8"))
+
+
+def _canon(value: object) -> str:
+    return json.dumps(value, sort_keys=True, separators=(",", ":"))
+
+
+def render_branch(branch: str) -> dict:
+    """The branch ruleset body for ``branch``: ``protect-master.json`` with the name
+    and the ref changed, nothing else."""
+    if not branch or "*" in branch or "~" in branch or branch.startswith("refs/"):
+        raise ValueError(f"not a plain branch name: {branch!r}")
+    body = _load(BRANCH_RULES_FILE)
+    body["name"] = f"protect-{branch}"
+    body["conditions"]["ref_name"]["include"] = [f"refs/heads/{branch}"]
+    return body
+
+
+def render_tags() -> dict:
+    """The release-tag ruleset body, exactly as the file holds it."""
+    return _load(TAG_RULES_FILE)
+
+
+def branch_set(default_branch: str, existing: object) -> list[str]:
+    """The branches to protect: ``integration`` and ``master`` where they exist, plus
+    the default branch, each once, in write order."""
+    if not default_branch:
+        raise ValueError("a repo with no default branch has no branch set")
+    names = [b for b in FIXED_BRANCHES if b in set(existing)]
+    if default_branch not in names:
+        names.append(default_branch)
+    return names
+
+
+def plan_bodies(branches: list[str]) -> list[dict]:
+    """Every body in write order: the tag ruleset, ``integration``, ``master``, then
+    any other branch."""
+    wanted = list(dict.fromkeys(branches))
+    ordered = [b for b in FIXED_BRANCHES if b in wanted]
+    ordered += [b for b in wanted if b not in FIXED_BRANCHES]
+    return [render_tags()] + [render_branch(b) for b in ordered]
+
+
+def payload_digest(bodies: list[dict]) -> str:
+    """The sha256 of the bodies in order; ``--confirm`` must repeat it."""
+    return hashlib.sha256(_canon(bodies).encode("utf-8")).hexdigest()
+
+
+def _set_diff(key: str, want: object, got: object) -> list[str]:
+    wanted = {_canon(x) for x in (want or [])}
+    found = {_canon(x) for x in (got or [])}
+    out = [f"{key}: missing {item}" for item in sorted(wanted - found)]
+    out += [f"{key}: extra {item}" for item in sorted(found - wanted)]
+    return out
+
+
+def compare_bodies(rendered: dict, remote: dict) -> list[str]:
+    """Differences between a body we rendered and the ruleset GitHub returned.
+
+    ``rules`` and ``bypass_actors`` compare as sets (a rule is its type plus its
+    complete parameters); the server keys in ``SERVER_KEYS`` are ignored; any other
+    key on either side is a difference. An empty list means equal.
+    """
+    kept = {k: v for k, v in remote.items() if k not in SERVER_KEYS}
+    diffs: list[str] = []
+    for key in sorted(set(rendered) | set(kept)):
+        if key not in kept:
+            diffs.append(f"{key}: missing in the remote ruleset")
+        elif key not in rendered:
+            diffs.append(f"{key}: unexpected key in the remote ruleset")
+        elif key in _SET_KEYS:
+            diffs.extend(_set_diff(key, rendered[key], kept[key]))
+        elif rendered[key] != kept[key]:
+            diffs.append(
+                f"{key}: expected {_canon(rendered[key])}, got {_canon(kept[key])}"
+            )
+    return diffs
diff --git a/tests/org_rulesets/__init__.py b/tests/org_rulesets/__init__.py
new file mode 100644
index 000000000..e69de29bb
diff --git a/tests/org_rulesets/conftest.py b/tests/org_rulesets/conftest.py
new file mode 100644
index 000000000..bd1a1dea3
--- /dev/null
+++ b/tests/org_rulesets/conftest.py
@@ -0,0 +1,32 @@
+"""Shared test support for scripts/apply_org_rulesets.py.
+
+Tests never call GitHub: every ``gh`` call goes through a fake runner defined here that
+answers from canned replies. Names are synthetic (``acme-one``). Every shared fixture is
+defined in this file only: a fixture imported into several test modules is listed more
+than once by ``pytest --fixtures``, which crashes on the tie (CI runs that command).
+"""
+
+from __future__ import annotations
+
+import importlib.util
+import sys
+from pathlib import Path
+
+import pytest
+
+ROOT = Path(__file__).resolve().parents[2]
+SCRIPT = ROOT / "scripts" / "apply_org_rulesets.py"
+
+
+def load_script():
+    spec = importlib.util.spec_from_file_location("apply_org_rulesets", SCRIPT)
+    mod = importlib.util.module_from_spec(spec)
+    sys.modules["apply_org_rulesets"] = mod
+    spec.loader.exec_module(mod)
+    return mod
+
+
+@pytest.fixture(scope="session")
+def orr():
+    """The script module, loaded once."""
+    return load_script()
diff --git a/tests/org_rulesets/test_render.py b/tests/org_rulesets/test_render.py
new file mode 100644
index 000000000..047e90172
--- /dev/null
+++ b/tests/org_rulesets/test_render.py
@@ -0,0 +1,169 @@
+"""Rendering, branch set, digest and comparison (pure functions, no process)."""
+
+from __future__ import annotations
+
+import copy
+import json
+from pathlib import Path
+
+import pytest
+
+RULES = Path(__file__).resolve().parents[2] / ".github" / "rulesets"
+
+
+def parsed(name):
+    return json.loads((RULES / name).read_text(encoding="utf-8"))
+
+
+def test_branch_bodies_equal_the_files(orr):
+    assert orr.render_branch("master") == parsed("protect-master.json")
+    assert orr.render_branch("integration") == parsed("protect-integration.json")
+
+
+def test_tag_body_equals_the_file_and_has_the_update_rule(orr):
+    body = orr.render_tags()
+    assert body == parsed("protect-release-tags.json")
+    types = {rule["type"] for rule in body["rules"]}
+    assert types == {"deletion", "non_fast_forward", "update"}
+
+
+def test_other_branch_changes_only_name_and_ref(orr):
+    body = orr.render_branch("main")
+    expected = parsed("protect-master.json")
+    expected["name"] = "protect-main"
+    expected["conditions"]["ref_name"]["include"] = ["refs/heads/main"]
+    assert body == expected
+
+
+@pytest.mark.parametrize(
+    "bad", ["", "feat/*", "a~b", "refs/heads/x", "~DEFAULT_BRANCH"]
+)
+def test_bad_branch_names_raise(orr, bad):
+    with pytest.raises(ValueError):
+        orr.render_branch(bad)
+
+
+def test_no_body_holds_the_default_branch_placeholder(orr):
+    bodies = orr.plan_bodies(["main", "master", "integration"])
+    assert "~DEFAULT_BRANCH" not in json.dumps(bodies)
+
+
+def test_render_returns_a_fresh_copy(orr):
+    first = orr.render_branch("master")
+    first["rules"].clear()
+    assert orr.render_branch("master")["rules"]
+
+
+@pytest.mark.parametrize(
+    ("default", "existing", "expected"),
+    [
+        ("master", {"master"}, ["master"]),
+        ("main", {"master"}, ["master", "main"]),
+        ("integration", {"integration", "master"}, ["integration", "master"]),
+        ("main", {"integration", "master"}, ["integration", "master", "main"]),
+    ],
+)
+def test_branch_set(orr, default, existing, expected):
+    got = orr.branch_set(default, existing)
+    assert got == expected
+    assert len(got) == len(set(got))
+
+
+def test_branch_set_refuses_an_empty_default(orr):
+    with pytest.raises(ValueError):
+        orr.branch_set("", {"master"})
+
+
+def test_plan_bodies_order(orr):
+    names = [b["name"] for b in orr.plan_bodies(["main", "master", "integration"])]
+    assert names == [
+        "protect-release-tags",
+        "protect-integration",
+        "protect-master",
+        "protect-main",
+    ]
+
+
+def test_plan_bodies_does_not_repeat_a_branch(orr):
+    names = [b["name"] for b in orr.plan_bodies(["master", "master"])]
+    assert names == ["protect-release-tags", "protect-master"]
+
+
+def test_digest_is_stable_and_sensitive(orr):
+    bodies = orr.plan_bodies(["master", "integration"])
+    assert orr.payload_digest(bodies) == orr.payload_digest(copy.deepcopy(bodies))
+    changed = copy.deepcopy(bodies)
+    changed[1]["enforcement"] = "evaluate"
+    assert orr.payload_digest(changed) != orr.payload_digest(bodies)
+    assert orr.payload_digest(list(reversed(bodies))) != orr.payload_digest(bodies)
+
+
+SERVER = {
+    "id": 7,
+    "source": "acme-one",
+    "source_type": "Repository",
+    "node_id": "RRS_x",
+    "created_at": "2026-01-01T00:00:00Z",
+    "updated_at": "2026-01-02T00:00:00Z",
+    "current_user_can_bypass": "never",
+    "_links": {"self": {"href": "https://example.invalid"}},
+}
+
+
+def test_compare_equal_and_server_keys_ignored(orr):
+    body = orr.render_branch("master")
+    assert orr.compare_bodies(body, copy.deepcopy(body)) == []
+    assert orr.compare_bodies(body, {**copy.deepcopy(body), **SERVER}) == []
+
+
+def test_compare_ignores_rule_and_actor_order(orr):
+    body = orr.render_branch("master")
+    remote = copy.deepcopy(body)
+    remote["rules"].reverse()
+    remote["bypass_actors"].reverse()
+    assert orr.compare_bodies(body, remote) == []
+
+
+def _diff(orr, mutate):
+    body = orr.render_branch("master")
+    remote = copy.deepcopy(body)
+    mutate(remote)
+    return "\n".join(orr.compare_bodies(body, remote))
+
+
+def test_compare_names_each_kind_of_difference(orr):
+    extra_rule = _diff(
+        orr, lambda r: r["rules"].append({"type": "required_signatures"})
+    )
+    assert "required_signatures" in extra_rule
+
+    extra_actor = _diff(
+        orr,
+        lambda r: r["bypass_actors"].append(
+            {"actor_id": 1, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}
+        ),
+    )
+    assert "OrganizationAdmin" in extra_actor
+
+    def reviews(r):
+        r["rules"][2]["parameters"]["required_approving_review_count"] = 2
+
+    assert "required_approving_review_count" in _diff(orr, reviews)
+
+    assert "enforcement" in _diff(orr, lambda r: r.update(enforcement="disabled"))
+
+    def other_ref(r):
+        r["conditions"]["ref_name"]["include"] = ["refs/heads/other"]
+
+    assert "conditions" in _diff(orr, other_ref)
+    assert "surprise" in _diff(orr, lambda r: r.update(surprise=True))
+
+
+def test_compare_reports_a_missing_rule(orr):
+    assert "deletion" in _diff(orr, lambda r: r["rules"].pop(0))
+
+
+def test_rendering_does_not_depend_on_the_working_folder(orr, tmp_path, monkeypatch):
+    before = (orr.render_branch("integration"), orr.render_tags())
+    monkeypatch.chdir(tmp_path)
+    assert (orr.render_branch("integration"), orr.render_tags()) == before

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
