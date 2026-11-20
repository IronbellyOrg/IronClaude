8b3599fca68bf0a3c6393f3dc8e6e5ee89857321
Review one task for spec compliance.

Task brief: ## Task 20: Create the trigger label on a repo when missing and check the Approved field

Create `src/superclaude/cli/issue_watch/repo_init.py` with a function that lists the repo's labels (`gh label list --repo <owner/name>`) and creates `issue-watch:trigger` with `gh label create --repo <owner/name>` when absent (requirements R11 and R35; the approval is the `Approved` issue field, not a label). It is idempotent and reports `created`, `present` or `failed` for the label. A second read-only check lists the owner's organization issue fields (`gh api --method GET orgs/<owner>/issue-fields`) and reports `approved_field_present` when a single-select field `Approved` with the option `Yes` exists, else `approved_field_missing` (or `failed` when the read fails); the module never creates the field, which is an organization setting for the owner. The names come from Task 17. Only the per-repo first run (Task 21) calls the creating function; the loop of Tasks 23 and 24 only reports a missing label (R14). This module is one of the two allowed GitHub writers named in Constraints; the coordinator-only guard class of Task 13 applies to launched agents, not to this cron-run module.

Depends on: Task 12, Task 17

Acceptance criteria:
- T20.AC1: New `tests/issue_watch/test_repo_init.py` covers: the trigger label missing (one create call), present (no create call), a failed create, and the `Approved` field present, missing, present without the option `Yes`, and a failed organization read.
- T20.AC2: `tests/issue_watch/test_security_invariants.py` still passes with `repo_init.py` named as an allowed writer (Task 12 documents the scope).
- T20.AC3: The label names are read from the defaults of Task 17, not written as literals in the module.
Global constraints: ## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- This plan applies requirement R35 (owner decision of 2026-11-19): the approval is no longer the label `issue-watch:approved`. It is the organization issue field `Approved` (single select, one option `Yes`, field id 50144115 on `IronbellyOrg`) set to `Yes` by an allowed approver (IronBelly, Clay or a maintainer, the approvers file of today). The trigger label `issue-watch:trigger` stays. Who set the field and when comes from the issue's GraphQL timeline events `IssueFieldAddedEvent`, `IssueFieldChangedEvent` and `IssueFieldRemovedEvent` (each carries `actor`, `createdAt`, `issueField` and the value; verified read-only on 2026-11-19 against issue 675 with another field), because the REST events endpoint names the event but not the field or the value. Task 4a builds the read; the approval predicates, the approval-void rule and the claim-time refusal keep their logic and see the field events as label events named by `approval_label`. A real label with the old name never approves. Task 4 is amended to observe the field instead of the label; the plan was copied from `TASK-WF-requirements-20261119-143917` (Tasks 1 to 3 complete there) and edited by owner instruction, and `source.md` still carries the label wording of the requirements file (Task 28 updates the requirements file).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval (the `Approved` issue field set to Yes, R35), the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the `Approved` field after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 4a, 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 4a, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 4a, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.
Start sha: 8b3599fca68bf0a3c6393f3dc8e6e5ee89857321
Diff against the start snapshot: diff --git a/tests/issue_watch/test_module_boundaries.py b/tests/issue_watch/test_module_boundaries.py
index b54c6e126..3917e6568 100644
--- a/tests/issue_watch/test_module_boundaries.py
+++ b/tests/issue_watch/test_module_boundaries.py
@@ -73,6 +73,8 @@ RULES: dict[str, Rule] = {
     "defaults": Rule(siblings=frozenset({"cycle", "github", "predicates"})),
     # plan Task 18: the Orca repo list; commands only through the Runner, no subprocess import.
     "repos": Rule(siblings=frozenset({"runner", "launch"})),
+    # plan Task 20: the trigger label and the Approved field check; the one watcher module that creates a label.
+    "repo_init": Rule(siblings=frozenset({"defaults", "github", "runner"})),
     # plan Task 19: one repo's generated config; reads through the Runner, writes two files.
     "generate": Rule(
         siblings=frozenset({"cycle", "defaults", "github", "repos", "runner"})
diff --git a/tests/issue_watch/test_security_invariants.py b/tests/issue_watch/test_security_invariants.py
index 1e4463bc6..7d6d4e774 100644
--- a/tests/issue_watch/test_security_invariants.py
+++ b/tests/issue_watch/test_security_invariants.py
@@ -1061,7 +1061,9 @@ def test_dispatch_json_entries_keep_their_keys_with_the_pipeline_none_prompt(tmp
 
 _WRITER_MODULES = {"complete.py", "repo_init.py"}
 _SRC = Path(__file__).resolve().parents[2] / "src/superclaude/cli"
-_WRITE_SIGN = re.compile(r'"POST"|"PUT"|"PATCH"|"DELETE"|\bmutation\s*[({]')
+_WRITE_SIGN = re.compile(
+    r'"POST"|"PUT"|"PATCH"|"DELETE"|\bmutation\s*[({]|"label",\s*"create"'
+)
 
 
 def test_only_complete_and_repo_init_may_write_to_github():
@@ -1071,7 +1073,7 @@ def test_only_complete_and_repo_init_may_write_to_github():
     assert {p.name for p in scanned} >= {"github.py", "cycle.py", "complete.py"}
     writers = {p.name for p in scanned if _WRITE_SIGN.search(p.read_text("utf-8"))}
     assert writers <= _WRITER_MODULES, writers
-    assert "complete.py" in writers  # the scan is not vacuous
+    assert {"complete.py", "repo_init.py"} <= writers  # the scan is not vacuous
     # github.py and the cycle stay read-only
     for name in ("github.py", "cycle.py"):
         assert name not in writers
diff --git a/src/superclaude/cli/issue_watch/repo_init.py b/src/superclaude/cli/issue_watch/repo_init.py
new file mode 100644
index 000000000..7a936e138
--- /dev/null
+++ b/src/superclaude/cli/issue_watch/repo_init.py
@@ -0,0 +1,147 @@
+"""Create the trigger label on a repository and check the ``Approved`` field (plan Task 20).
+
+This module and ``issue_pipeline/complete.py`` are the only code that writes to GitHub. Only the
+per-repo first run (Task 21) calls ``ensure_trigger_label``, which creates the label when it is
+missing; the loop that runs from cron only calls ``trigger_label_state``, which reads (R14).
+
+The approval is the organization issue field ``Approved`` set to ``Yes`` (R35), not a label. This
+module only checks that the field and its option exist (``check_approved_field``, a read); it
+never creates the field, which is an organization setting for the owner.
+
+The label, field and option names come from the central defaults (Task 17), never from literals
+here. Every command runs through the ``Runner`` (an argv list, no shell).
+
+[UNVERIFIED] The reply shape of ``GET orgs/<owner>/issue-fields`` is read defensively: a list of
+fields, or an object holding one under ``fields``, each with a ``name``, a type word that holds
+``single_select`` and a list of ``options`` with a ``name``. Anything else is ``failed``.
+"""
+
+from __future__ import annotations
+
+import json
+import re
+
+from .defaults import Defaults
+from .github import _repo_arg
+from .runner import CommandResult, Runner
+
+TIMEOUT_S = 30.0
+LABEL_LIMIT = 500
+LABEL_COLOR = "0E8A16"
+LABEL_DESCRIPTION = "The issue watcher may claim this issue once it is approved"
+
+CREATED = "created"
+PRESENT = "present"
+MISSING = "missing"
+FAILED = "failed"
+FIELD_PRESENT = "approved_field_present"
+FIELD_MISSING = "approved_field_missing"
+
+_OWNER = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
+
+
+def _ok(result: CommandResult) -> bool:
+    return not (
+        result.timed_out or result.spawn_error is not None or result.returncode != 0
+    )
+
+
+def _json(result: CommandResult) -> object | None:
+    if not _ok(result):
+        return None
+    try:
+        return json.loads(result.stdout)
+    except ValueError:
+        return None
+
+
+def argv_label_list(repo: str) -> list[str]:
+    return [
+        "gh",
+        "label",
+        "list",
+        "--repo",
+        _repo_arg(repo),
+        "--json",
+        "name",
+        "--limit",
+        str(LABEL_LIMIT),
+    ]
+
+
+def argv_label_create(repo: str, label: str) -> list[str]:
+    return [
+        "gh",
+        "label",
+        "create",
+        label,
+        "--repo",
+        _repo_arg(repo),
+        "--color",
+        LABEL_COLOR,
+        "--description",
+        LABEL_DESCRIPTION,
+    ]
+
+
+def argv_issue_fields(owner: str) -> list[str]:
+    if not _OWNER.fullmatch(owner):
+        raise ValueError("invalid owner")
+    return ["gh", "api", "--method", "GET", f"orgs/{owner}/issue-fields"]
+
+
+def trigger_label_state(repo: str, defaults: Defaults, runner: Runner) -> str:
+    """``present``, ``missing`` or ``failed``; reads only, never creates (the cron loop, R14)."""
+    data = _json(runner.run(argv_label_list(repo), TIMEOUT_S))
+    if not isinstance(data, list) or not all(
+        isinstance(row, dict) and isinstance(row.get("name"), str) for row in data
+    ):
+        return FAILED
+    if len(data) >= LABEL_LIMIT:
+        return (
+            FAILED  # a full list may hide the label; do not create a duplicate blindly
+        )
+    names = {row["name"] for row in data}
+    return PRESENT if defaults.trigger_label in names else MISSING
+
+
+def ensure_trigger_label(repo: str, defaults: Defaults, runner: Runner) -> str:
+    """Create the trigger label when it is missing; ``created``, ``present`` or ``failed``.
+
+    Idempotent: a present label makes no create call. Only the first run calls this.
+    """
+    state = trigger_label_state(repo, defaults, runner)
+    if state != MISSING:
+        return state  # PRESENT or FAILED
+    created = runner.run(argv_label_create(repo, defaults.trigger_label), TIMEOUT_S)
+    return CREATED if _ok(created) else FAILED
+
+
+def _fields(data: object) -> list[object] | None:
+    if isinstance(data, list):
+        return data
+    if isinstance(data, dict) and isinstance(data.get("fields"), list):
+        return data["fields"]
+    return None
+
+
+def check_approved_field(owner: str, defaults: Defaults, runner: Runner) -> str:
+    """``approved_field_present``, ``approved_field_missing`` or ``failed``; a read.
+
+    Present means a single-select field named ``defaults.approval_field`` that has the option
+    ``defaults.approval_option``. The field is never created here.
+    """
+    fields = _fields(_json(runner.run(argv_issue_fields(owner), TIMEOUT_S)))
+    if fields is None:
+        return FAILED
+    for field in fields:
+        if not isinstance(field, dict) or field.get("name") != defaults.approval_field:
+            continue
+        kind = str(field.get("data_type") or field.get("type") or "").lower()
+        options = field.get("options")
+        if "single_select" not in kind or not isinstance(options, list):
+            continue
+        names = {o.get("name") for o in options if isinstance(o, dict)}
+        if defaults.approval_option in names:
+            return FIELD_PRESENT
+    return FIELD_MISSING
diff --git a/tests/issue_watch/test_repo_init.py b/tests/issue_watch/test_repo_init.py
new file mode 100644
index 000000000..a6c6e3e78
--- /dev/null
+++ b/tests/issue_watch/test_repo_init.py
@@ -0,0 +1,203 @@
+"""Task 20: the trigger label and the ``Approved`` field check, over a scripted ``gh``."""
+
+from __future__ import annotations
+
+import json
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_watch import defaults, repo_init
+
+from .conftest import result
+
+REPO = "IronbellyOrg/IronClaude"
+DEFAULTS = defaults.Defaults()
+LABEL = DEFAULTS.trigger_label
+
+
+class Gh:
+    """A scripted runner keyed by argv; it records every call."""
+
+    def __init__(self, script: dict) -> None:
+        self.script = script
+        self.calls: list[tuple[str, ...]] = []
+
+    def run(self, argv, timeout, *, cwd=None):
+        key = tuple(argv)
+        self.calls.append(key)
+        assert key in self.script, f"unscripted argv: {argv}"
+        return self.script[key]
+
+
+def _labels(*names: str):
+    return result(stdout=json.dumps([{"name": n} for n in names]))
+
+
+def _creates(gh: Gh) -> list[tuple[str, ...]]:
+    return [c for c in gh.calls if c[:3] == ("gh", "label", "create")]
+
+
+def test_a_missing_label_is_created_with_one_create_call() -> None:
+    gh = Gh(
+        {
+            tuple(repo_init.argv_label_list(REPO)): _labels("bug", "feature"),
+            tuple(repo_init.argv_label_create(REPO, LABEL)): result(),
+        }
+    )
+    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "created"
+    assert _creates(gh) == [tuple(repo_init.argv_label_create(REPO, LABEL))]
+
+
+def test_a_present_label_makes_no_create_call() -> None:
+    gh = Gh({tuple(repo_init.argv_label_list(REPO)): _labels("bug", LABEL)})
+    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "present"
+    assert _creates(gh) == []
+
+
+def test_a_second_call_after_a_create_is_idempotent() -> None:
+    state = {"labels": ["bug"]}
+
+    class World(Gh):
+        def run(self, argv, timeout, *, cwd=None):
+            self.calls.append(tuple(argv))
+            if argv[:3] == ["gh", "label", "list"]:
+                return _labels(*state["labels"])
+            state["labels"].append(argv[3])
+            return result()
+
+    gh = World({})
+    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "created"
+    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "present"
+    assert len(_creates(gh)) == 1
+
+
+def test_a_failed_create_is_reported_failed() -> None:
+    gh = Gh(
+        {
+            tuple(repo_init.argv_label_list(REPO)): _labels("bug"),
+            tuple(repo_init.argv_label_create(REPO, LABEL)): result(
+                stderr="HTTP 403", returncode=1
+            ),
+        }
+    )
+    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "failed"
+
+
+@pytest.mark.parametrize(
+    "reply",
+    [
+        result(stderr="HTTP 502", returncode=1),
+        result(timed_out=True),
+        result(spawn_error="FileNotFoundError"),
+        result(stdout="not json"),
+        result(stdout='{"name": "x"}'),
+        result(stdout='[{"nome": "x"}]'),
+        result(stdout=json.dumps([{"name": f"l{i}"} for i in range(500)])),
+    ],
+)
+def test_a_failed_or_unreadable_or_full_list_never_creates(reply) -> None:
+    gh = Gh({tuple(repo_init.argv_label_list(REPO)): reply})
+    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "failed"
+    assert _creates(gh) == []
+
+
+def test_the_read_only_state_check_never_creates() -> None:
+    gh = Gh({tuple(repo_init.argv_label_list(REPO)): _labels("bug")})
+    assert repo_init.trigger_label_state(REPO, DEFAULTS, gh) == "missing"
+    assert _creates(gh) == []
+    gh = Gh({tuple(repo_init.argv_label_list(REPO)): _labels(LABEL)})
+    assert repo_init.trigger_label_state(REPO, DEFAULTS, gh) == "present"
+
+
+def test_the_label_name_comes_from_the_defaults() -> None:
+    custom = defaults.Defaults(trigger_label="watch:go")
+    gh = Gh(
+        {
+            tuple(repo_init.argv_label_list(REPO)): _labels(
+                LABEL
+            ),  # the built-in is NOT it
+            tuple(repo_init.argv_label_create(REPO, "watch:go")): result(),
+        }
+    )
+    assert repo_init.ensure_trigger_label(REPO, custom, gh) == "created"
+    assert _creates(gh)[0][3] == "watch:go"
+
+
+def test_no_name_is_a_literal_in_the_module() -> None:
+    source = Path(repo_init.__file__).read_text()
+    for literal in ("issue-watch:trigger", '"Approved"', '"Yes"'):
+        assert literal not in source
+
+
+@pytest.mark.parametrize("bad", ["a/b/c", "", "a b/c", "-a/b"])
+def test_a_bad_repo_raises_before_any_call(bad) -> None:
+    gh = Gh({})
+    with pytest.raises(ValueError):
+        repo_init.ensure_trigger_label(bad, DEFAULTS, gh)
+    assert gh.calls == []
+
+
+# --- the Approved field ------------------------------------------------------------------
+
+
+def _fields(*rows: dict):
+    return result(stdout=json.dumps(list(rows)))
+
+
+def _approved(options=("Yes",), kind="single_select", name="Approved") -> dict:
+    return {
+        "name": name,
+        "data_type": kind,
+        "options": [{"name": o} for o in options],
+    }
+
+
+def _check(reply) -> str:
+    argv = tuple(repo_init.argv_issue_fields("IronbellyOrg"))
+    gh = Gh({argv: reply})
+    out = repo_init.check_approved_field("IronbellyOrg", DEFAULTS, gh)
+    assert gh.calls == [argv]  # one read, nothing else
+    return out
+
+
+def test_the_approved_field_present_with_the_yes_option() -> None:
+    assert _check(_fields(_approved(), {"name": "Other"})) == "approved_field_present"
+    # the object form with a "fields" list is read too
+    obj = result(stdout=json.dumps({"fields": [_approved(("No", "Yes"))]}))
+    assert _check(obj) == "approved_field_present"
+
+
+def test_the_approved_field_missing() -> None:
+    assert _check(_fields({"name": "Other"})) == "approved_field_missing"
+    assert _check(_fields()) == "approved_field_missing"
+
+
+def test_the_approved_field_present_without_the_yes_option() -> None:
+    assert _check(_fields(_approved(("No", "Maybe")))) == "approved_field_missing"
+    assert _check(_fields(_approved(()))) == "approved_field_missing"
+
+
+def test_a_field_named_approved_that_is_not_single_select_does_not_count() -> None:
+    assert _check(_fields(_approved(kind="text"))) == "approved_field_missing"
+
+
+@pytest.mark.parametrize(
+    "reply",
+    [
+        result(stderr="HTTP 404", returncode=1),
+        result(timed_out=True),
+        result(stdout="not json"),
+        result(stdout='"a string"'),
+    ],
+)
+def test_a_failed_organization_read_is_reported_failed(reply) -> None:
+    assert _check(reply) == "failed"
+
+
+def test_the_field_check_never_writes() -> None:
+    argv = repo_init.argv_issue_fields("IronbellyOrg")
+    assert argv == ["gh", "api", "--method", "GET", "orgs/IronbellyOrg/issue-fields"]
+    for bad in ("a/b", "", "-x", "a b"):
+        with pytest.raises(ValueError):
+            repo_init.argv_issue_fields(bad)

Task 20 context. repo_init.py is new. It has two entry points on purpose: ensure_trigger_label (creates; only the first run calls it) and trigger_label_state (read only; the cron loop uses it, R14). The security scan of test_security_invariants.py now also recognises a gh label create and asserts repo_init.py is among the writers. The reply shape of `GET orgs/<owner>/issue-fields` is not verified live, so it is read defensively and anything unexpected is `failed`. Tests run: tests/issue_watch 2943 passed; ruff clean; make verify-sync clean.

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
