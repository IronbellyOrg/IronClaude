ead53a8a2644bd9e8c6f5e44f0b826018cc00c5c
Review one task for spec compliance.

Task brief: ## Task 17: Read the central defaults file

Create `src/superclaude/cli/issue_watch/defaults.py`. It reads `issue-watch-defaults.json` from a config directory passed in (default `~/.config/superclaude`; the file the Coder template saves, requirement R1) and returns the fixed approver logins, the trigger label name, the approval field name and option (R35), the allowed repo owners and an optional map from `owner/name` to a Project node id. When the file is absent it returns built-in values: approver logins `ironbelly` and `clayphi`, trigger label `issue-watch:trigger`, approval field `Approved` with option `Yes`, allowed owner `IronbellyOrg`, an empty map. Unknown keys, a wrong type or a bad login are rejected with the existing `ConfigError` style (`cycle.py` line 81). The module is pure: it reads one file and runs no command.

Acceptance criteria:
- T17.AC1: New `tests/issue_watch/test_defaults.py` covers: file absent, a valid file, an unknown key, a bad login such as `-x`, and a map entry whose id does not match `PVT_`; every path is under `tmp_path`.
- T17.AC2: `tests/issue_watch/test_module_boundaries.py` passes with the new module.
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
Start sha: ead53a8a2644bd9e8c6f5e44f0b826018cc00c5c
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/defaults.py b/src/superclaude/cli/issue_watch/defaults.py
new file mode 100644
index 000000000..a7efe096e
--- /dev/null
+++ b/src/superclaude/cli/issue_watch/defaults.py
@@ -0,0 +1,149 @@
+"""The central defaults of the issue watcher (plan Task 17, requirement R1).
+
+``issue-watch-defaults.json`` is the file the Coder template saves under the config
+directory (``~/.config/superclaude`` by default). It holds the values every repository
+shares: who may approve, the trigger label, the approval issue field, the owners whose
+repositories may be served and an optional map from ``owner/name`` to a Project node id.
+
+This module is pure: it reads that one file and runs no command. A key the file leaves out
+takes its built-in value, and an absent file gives the built-ins. Unknown keys, a wrong
+type, a bad login, a bad repository name or a Project id that is not ``PVT_...`` raise
+``ConfigError("config_invalid")`` with a fixed detail text that never quotes the file.
+"""
+
+from __future__ import annotations
+
+import json
+import re
+from dataclasses import dataclass, field
+from pathlib import Path
+
+from .cycle import ConfigError
+from .github import valid_repo
+from .predicates import APPROVAL_FIELD_NAME, APPROVAL_FIELD_VALUE
+
+DEFAULTS_FILE = "issue-watch-defaults.json"
+DEFAULT_CONFIG_DIR = "~/.config/superclaude"
+
+BUILTIN_APPROVER_LOGINS = ("ironbelly", "clayphi")
+BUILTIN_TRIGGER_LABEL = "issue-watch:trigger"
+BUILTIN_ALLOWED_OWNERS = ("IronbellyOrg",)
+
+_KEYS = frozenset(
+    {
+        "approver_logins",
+        "trigger_label",
+        "approval_field",
+        "approval_option",
+        "allowed_owners",
+        "projects",
+    }
+)
+_MAX_BYTES = 64 * 1024
+_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
+_OWNER = _LOGIN
+_PROJECT_ID = re.compile(r"PVT_[A-Za-z0-9_-]{1,64}")
+_NAME_MAX = 50
+
+
+@dataclass(frozen=True)
+class Defaults:
+    """The validated central defaults."""
+
+    approver_logins: tuple[str, ...] = BUILTIN_APPROVER_LOGINS
+    trigger_label: str = BUILTIN_TRIGGER_LABEL
+    approval_field: str = APPROVAL_FIELD_NAME
+    approval_option: str = APPROVAL_FIELD_VALUE
+    allowed_owners: tuple[str, ...] = BUILTIN_ALLOWED_OWNERS
+    projects: dict[str, str] = field(default_factory=dict)
+    """``owner/name`` to a Project node id; empty by default."""
+
+
+def _invalid(detail: str) -> ConfigError:
+    return ConfigError("config_invalid", f"{DEFAULTS_FILE}: {detail}")
+
+
+def _name(value: object, key: str) -> str:
+    """A short single-line name with no comma, no control character and no leading dash."""
+    if (
+        not isinstance(value, str)
+        or not 0 < len(value) <= _NAME_MAX
+        or value.startswith("-")
+        or "," in value
+        or any(ord(c) < 32 or ord(c) == 127 for c in value)
+    ):
+        raise _invalid(f"{key} must be a short single-line name")
+    return value
+
+
+def _logins(value: object, key: str, pattern: re.Pattern[str]) -> tuple[str, ...]:
+    if (
+        not isinstance(value, list)
+        or not value
+        or not all(isinstance(v, str) and pattern.fullmatch(v) for v in value)
+    ):
+        raise _invalid(f"{key} must be a non-empty list of GitHub names")
+    if len({v.lower() for v in value}) != len(value):
+        raise _invalid(f"{key} must not repeat a name")
+    return tuple(value)
+
+
+def _projects(value: object) -> dict[str, str]:
+    if not isinstance(value, dict):
+        raise _invalid("projects must be an object of owner/name to a PVT_ id")
+    for repo, project_id in value.items():
+        if not valid_repo(repo):
+            raise _invalid("a projects key must be owner/name")
+        if not isinstance(project_id, str) or not _PROJECT_ID.fullmatch(project_id):
+            raise _invalid("a projects value must be a PVT_ Project node id")
+    return dict(value)
+
+
+def load_defaults(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Defaults:
+    """Read ``issue-watch-defaults.json`` from ``config_dir``; the built-ins when it is absent.
+
+    Reads one file and runs no command. A present file that cannot be read or parsed, or that
+    holds an unknown key or a bad value, raises ``ConfigError("config_invalid")``.
+    """
+    path = Path(config_dir).expanduser() / DEFAULTS_FILE
+    try:
+        if not path.is_file():
+            if path.exists() or path.is_symlink():
+                raise _invalid("it is not a regular file")
+            return Defaults()
+        with open(path, "rb") as handle:
+            data = handle.read(_MAX_BYTES + 1)
+    except ConfigError:
+        raise
+    except OSError:
+        raise _invalid("it cannot be read") from None
+    if len(data) > _MAX_BYTES:
+        raise _invalid("it is larger than 64 KiB")
+    try:
+        raw = json.loads(data)
+    except (ValueError, RecursionError):  # ValueError covers bad JSON and UTF-8
+        raise _invalid("it is not valid JSON") from None
+    if not isinstance(raw, dict):
+        raise _invalid("it must be a JSON object")
+    unknown = set(raw) - _KEYS
+    if unknown:
+        raise _invalid("it holds an unknown key")
+    base = Defaults()
+    return Defaults(
+        approver_logins=_logins(raw["approver_logins"], "approver_logins", _LOGIN)
+        if "approver_logins" in raw
+        else base.approver_logins,
+        trigger_label=_name(raw["trigger_label"], "trigger_label")
+        if "trigger_label" in raw
+        else base.trigger_label,
+        approval_field=_name(raw["approval_field"], "approval_field")
+        if "approval_field" in raw
+        else base.approval_field,
+        approval_option=_name(raw["approval_option"], "approval_option")
+        if "approval_option" in raw
+        else base.approval_option,
+        allowed_owners=_logins(raw["allowed_owners"], "allowed_owners", _OWNER)
+        if "allowed_owners" in raw
+        else base.allowed_owners,
+        projects=_projects(raw["projects"]) if "projects" in raw else {},
+    )
diff --git a/tests/issue_watch/test_defaults.py b/tests/issue_watch/test_defaults.py
new file mode 100644
index 000000000..302dd47fc
--- /dev/null
+++ b/tests/issue_watch/test_defaults.py
@@ -0,0 +1,141 @@
+"""Task 17: the central defaults file; every path is under ``tmp_path``."""
+
+from __future__ import annotations
+
+import json
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_watch import cycle, defaults
+
+
+def _write(tmp_path: Path, raw: object) -> Path:
+    path = tmp_path / defaults.DEFAULTS_FILE
+    path.write_text(raw if isinstance(raw, str) else json.dumps(raw), encoding="utf-8")
+    return tmp_path
+
+
+def test_an_absent_file_gives_the_built_in_values(tmp_path: Path) -> None:
+    got = defaults.load_defaults(tmp_path)
+    assert got.approver_logins == ("ironbelly", "clayphi")
+    assert got.trigger_label == "issue-watch:trigger"
+    assert (got.approval_field, got.approval_option) == ("Approved", "Yes")
+    assert got.allowed_owners == ("IronbellyOrg",)
+    assert got.projects == {}
+    assert got == defaults.Defaults()
+
+
+def test_a_valid_file_is_read(tmp_path: Path) -> None:
+    _write(
+        tmp_path,
+        {
+            "approver_logins": ["ironbelly", "clayphi", "a-maintainer"],
+            "trigger_label": "watch:go",
+            "approval_field": "Approved",
+            "approval_option": "Yes",
+            "allowed_owners": ["IronbellyOrg", "Other-Org"],
+            "projects": {"IronbellyOrg/IronClaude": "PVT_kwDOabc-_1"},
+        },
+    )
+    got = defaults.load_defaults(tmp_path)
+    assert got.approver_logins == ("ironbelly", "clayphi", "a-maintainer")
+    assert got.trigger_label == "watch:go"
+    assert got.allowed_owners == ("IronbellyOrg", "Other-Org")
+    assert got.projects == {"IronbellyOrg/IronClaude": "PVT_kwDOabc-_1"}
+
+
+def test_a_key_the_file_leaves_out_takes_its_built_in_value(tmp_path: Path) -> None:
+    _write(tmp_path, {"trigger_label": "watch:go"})
+    got = defaults.load_defaults(tmp_path)
+    assert got.trigger_label == "watch:go"
+    assert got.approver_logins == defaults.BUILTIN_APPROVER_LOGINS
+    assert got.allowed_owners == defaults.BUILTIN_ALLOWED_OWNERS
+
+
+@pytest.mark.parametrize(
+    "raw",
+    [
+        {"surprise": 1},
+        {"approver_logins": ["-x"]},
+        {"approver_logins": ["ironbelly", "IronBelly"]},  # a repeat, whatever the case
+        {"approver_logins": []},
+        {"approver_logins": "ironbelly"},
+        {"approver_logins": ["a b"]},
+        {"approver_logins": [5]},
+        {"trigger_label": ""},
+        {"trigger_label": "-lead"},
+        {"trigger_label": "a,b"},
+        {"trigger_label": "x" * 51},
+        {"trigger_label": 3},
+        {"approval_field": "two\nlines"},
+        {"approval_option": None},
+        {"allowed_owners": ["bad owner"]},
+        {"allowed_owners": []},
+        {"projects": []},
+        {"projects": {"IronbellyOrg/IronClaude": "PVX_abc"}},
+        {"projects": {"IronbellyOrg/IronClaude": "PVT_"}},
+        {"projects": {"IronbellyOrg/IronClaude": 7}},
+        {"projects": {"not-a-repo": "PVT_abc"}},
+        {"projects": {"a/b/c": "PVT_abc"}},
+        [],
+        "not json at all",
+        '{"a": 1',
+        "\xff\xfe",
+    ],
+)
+def test_a_bad_file_is_rejected_with_the_config_error(tmp_path: Path, raw) -> None:
+    _write(tmp_path, raw)
+    with pytest.raises(cycle.ConfigError) as err:
+        defaults.load_defaults(tmp_path)
+    assert err.value.reason == "config_invalid"
+    assert defaults.DEFAULTS_FILE in err.value.detail
+
+
+def test_an_unknown_key_name_never_reaches_the_error_text(tmp_path: Path) -> None:
+    canary = "CANARY-17-KEY"
+    _write(tmp_path, {canary: 1})
+    with pytest.raises(cycle.ConfigError) as err:
+        defaults.load_defaults(tmp_path)
+    assert canary not in str(err.value) and canary not in err.value.detail
+
+
+def test_a_bad_login_never_reaches_the_error_text(tmp_path: Path) -> None:
+    canary = "CANARY-17-DO-NOT-ECHO;"
+    _write(tmp_path, {"approver_logins": [canary]})
+    with pytest.raises(cycle.ConfigError) as err:
+        defaults.load_defaults(tmp_path)
+    assert canary not in str(err.value) and canary not in err.value.detail
+
+
+def test_a_file_that_is_too_large_or_not_a_regular_file_is_rejected(
+    tmp_path: Path,
+) -> None:
+    big = tmp_path / "big"
+    big.mkdir()
+    _write(big, '{"trigger_label": "' + "x" * (70 * 1024) + '"}')
+    with pytest.raises(cycle.ConfigError):
+        defaults.load_defaults(big)
+    directory = tmp_path / "dir"
+    (directory / defaults.DEFAULTS_FILE).mkdir(parents=True)
+    with pytest.raises(cycle.ConfigError):
+        defaults.load_defaults(directory)
+
+
+def test_the_default_config_dir_is_expanded_and_runs_nothing(
+    tmp_path: Path, monkeypatch
+) -> None:
+    monkeypatch.setenv("HOME", str(tmp_path))
+    (tmp_path / ".config" / "superclaude").mkdir(parents=True)
+    _write(tmp_path / ".config" / "superclaude", {"trigger_label": "from:home"})
+    assert defaults.load_defaults().trigger_label == "from:home"
+    # nothing under tmp_path was written by the read
+    assert sorted(p.name for p in (tmp_path / ".config" / "superclaude").iterdir()) == [
+        defaults.DEFAULTS_FILE
+    ]
+
+
+def test_the_module_imports_no_process_module() -> None:
+    source = Path(defaults.__file__).read_text()
+    for banned in ("subprocess", "os.system", "shell=True"):
+        assert banned not in source

Re-review F1.1 only: the unknown-key detail is now fixed text. Also confirm no other detail in defaults.py is built from file text.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): ead53a8a2644bd9e8c6f5e44f0b826018cc00c5c
tree=none
F1.1 ac=scope at=src/superclaude/cli/issue_watch/defaults.py:130 anchor="cycle.py:89-90" chk=n,y,n,n family=detail-echo fix=use a fixed detail text for an unknown key sev=blocking trigger=B4 first=start origin=new: the unknown-key detail joined the file's key names although the docstring and ConfigError say it never quotes the file

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
