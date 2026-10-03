"""Workflow-owned task package lifecycle: contract scenarios.

Enforcement types (see each test):
  STATIC   - assertions over protocol Markdown (the agent follows these when inferring)
  CROSS    - docs examples evaluated against a reference algorithm and the shipped
             archive helper's identity regex (executable)
Real archive behavior is proven in tests/skills/test_workflow_archive.py.
"""

import importlib.util
import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_WF_REFS = _REPO / "src/superclaude/skills/sc-workflow-protocol/refs"
_HELPER = (
    _REPO / "src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py"
)
_spec = importlib.util.spec_from_file_location("archive_workspace_lc", _HELPER)
aw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aw)


def subject(source: str) -> str:
    """Reference implementation of the documented lower-camelCase subject algorithm."""
    ws = [w.lower() for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|[0-9]+", source)]
    if not ws or ws[0][0].isdigit():
        ws.insert(0, "plan")
    return (ws[0] + "".join(w.capitalize() for w in ws[1:]))[:16]


def _doc_examples():
    rows = []
    for line in (_WF_REFS / "input-parse.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| `([^`]+)` \| `([^`]+)`", line)
        if m and not m.group(1).startswith("E-"):
            rows.append((m.group(1), m.group(2)))
    return rows


def _basename_no_ext(x: str) -> str:
    return Path(x).stem if x.endswith(".md") else x


@pytest.mark.parametrize("source,expected", _doc_examples())
def test_documented_subject_examples_follow_the_stated_algorithm(
    source, expected
):  # CROSS
    assert subject(_basename_no_ext(source)) == expected


def test_doc_examples_cover_cap_and_fallback():  # CROSS
    ex = dict(_doc_examples())
    assert len(ex) >= 4 and "plan" in ex.values()
    assert any(len(v) == 16 for v in ex.values())


@pytest.mark.parametrize(
    "src,expected",
    [
        ("authLogin", "authLogin"),  # already camel is preserved
        ("XMLParser", "xmlParser"),  # acronym boundary
        ("snake_case_name", "snakeCaseName"),
        ("kebab-case-name", "kebabCaseName"),
        ("two words here", "twoWordsHere"),
        ("!!!", "plan"),  # punctuation only
        ("", "plan"),
        ("2fa login", "plan2FaLogin"),  # leading digit -> 'plan' prefix
        ("123", "plan123"),
        ("Ünïcode Café", "nCodeCaf"),
    ],
)
def test_subject_edge_cases(src, expected):  # CROSS
    assert subject(src) == expected
    assert aw.ID_RE.match(f"TASK-WF-{subject(src)}-20261001-063000")


def test_subject_truncates_to_16_and_always_matches_helper_regex():  # CROSS
    assert subject("a very long descriptive prompt title") == "aVeryLongDescrip"
    for n in range(1, 40):
        s = subject("word " * n)
        assert len(s) <= 16 and aw.ID_RE.match(f"TASK-WF-{s}-20261001-063000-2")


def test_tasklist_filename_is_full_id_basename_including_suffix():  # CROSS
    ident = "TASK-WF-authLogin-20261001-063000-2"
    assert (
        aw.ID_RE.match(ident)
        and f"{ident}.md" == "TASK-WF-authLogin-20261001-063000-2.md"
    )


@pytest.mark.parametrize("suffix", ["", "-2", "-9"])
def test_generated_ids_are_accepted_by_the_archive_helper(suffix):  # CROSS
    ident = f"TASK-WF-{subject('PRD_User Auth')}-20261001-063000{suffix}"
    assert aw.ID_RE.match(ident)


@pytest.mark.parametrize(
    "bad",
    [
        "TASK-WF-x-20261001-063000-1",
        "TASK-WF-x-20261001-063000-10",
        "TASK-WF-X-20261001-063000",
        "TASK-WF-auth-login-20261001-063000",  # hyphen in subject
        "TASK-WF-1abc-20261001-063000",  # leading digit
        "TASK-WF-abcdefghijklmnopq-20261001-063000",  # 17 chars
        "TASK-WF--20261001-063000",
        "task-wf-x-20261001-063000",
        "TASK-PRD-x-20261001-063000",
    ],
)
def test_helper_rejects_non_workflow_or_unbounded_suffix_ids(bad):  # CROSS
    assert not aw.ID_RE.match(bad)


def test_workflow_and_helper_agree_on_contract_and_schema():  # STATIC+CROSS
    contract = (_WF_REFS / "return-contract.md").read_text(encoding="utf-8")
    gates = (_WF_REFS / "quality-gates.md").read_text(encoding="utf-8")
    src = _HELPER.read_text(encoding="utf-8")
    assert 'contract_version: "1.1"' in contract and '"1.1"' in src
    assert "schema: workflow-plan/1.2" in gates and "workflow-plan/1.2" in src
    for status in (
        "success",
        "partial",
    ):  # helper accepts exactly the non-failed states
        assert status in contract
    assert '("success", "partial")' in src


def test_workflow_handoff_relocation_rule():  # STATIC
    skill = (_WF_REFS.parent / "SKILL.md").read_text(encoding="utf-8")
    contract = (_WF_REFS / "return-contract.md").read_text(encoding="utf-8")
    routing = (_WF_REFS / "overlap-routing.md").read_text(encoding="utf-8")
    assert "**before** any `implement` handoff" in skill
    for text in (skill, contract):
        assert "never recreate a directory" in text or "never write, recreate" in text
        assert "Both exist" in text or "both locations exist" in text
    assert "re-resolve it by id" in routing


# --- managed implement protocol (design R2-R5) ------------------------------------
_IMPL = _REPO / "src/superclaude/skills/sc-implement-protocol"
_IMPL_CMD = _REPO / "src/superclaude/commands/implement.md"


def _impl(name):
    return (_IMPL / name).read_text(encoding="utf-8")


def _managed():
    return _impl("refs/managed-workspace.md")


def test_managed_detection_requires_schema_slug_contract_and_checkout_location():  # STATIC
    m = _managed()
    for token in (
        "`schema: workflow-plan/1.2`",
        "equals the name of `P`'s parent directory",
        '`contract_version: "1.1"`',
        "`status: success` or `partial`",
        "`<checkout>/.dev/tasks/to-do/<slug>/<slug>.md` or `<checkout>/.dev/tasks/done/<slug>/<slug>.md`",
        "^TASK-WF-[a-z][A-Za-z0-9]{0,15}-[0-9]{8}-[0-9]{6}(-[2-9])?$",
        "A copied plan or a plan from another checkout fails here",
        "STOP `E-MANAGED-INVALID`",
        "Any other schema → legacy path",
    ):
        assert token in m, token
    skill = _impl("SKILL.md")
    assert "**Managed check first**" in skill and "refs/managed-workspace.md" in skill
    assert "workflow-plan/1.2" in skill
    for code in (
        "E-MANAGED-INVALID",
        "E-MANAGED-CONFLICT",
        "E-PLAN-CHANGED",
        "E-ARCHIVE-MARKER",
        "E-ARCHIVE-BLOCKED",
    ):
        assert f"`{code}`" in skill, code


def test_legacy_behavior_is_preserved():  # STATIC
    skill, ledger, qa = _impl("SKILL.md"), _impl("refs/ledger.md"), _impl("refs/qa.md")
    assert "`.dev/implement/<slug>/progress.md`" in skill
    assert "SHA-256 of the **absolute** path" in skill  # path-hashed legacy slug
    assert "Legacy sources" in skill and "Legacy: if all tasks already" in skill
    assert (
        "Closed enum: `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`."
        in qa
    )
    assert "^T([0-9A-Za-z.-]+): (complete|blocked) verdict=" in ledger
    assert "legacy-ledger" in ledger and "Legacy ledgers never contain them" in ledger


def test_managed_ledger_artifacts_and_pins_are_stable():  # STATIC
    m = _managed()
    for token in (
        "Ledger is always `<pkg>/progress.md`",
        "`E-LEDGER-PATH`",
        "refs/superclaude/implement/<slug>/T<id>",
        "No lookup hashes a plan path",
        "`<pkg>/artifacts/`",
        "`./artifacts/<file>:<line>`",
        "appending a new `PLAN:` line (append-only; never edit)",
        "The first `T<id>: start` line is the immutability boundary",
        "`E-PLAN-CHANGED`; no repair, no new pin",
        "`--no-promote`",
        "sole mover",
        "`<root>/adversarial/`",
        "realpath is inside `<pkg>/artifacts/`",
    ):
        assert token in m, token


def test_managed_final_and_archive_gate_rules():  # STATIC
    m = _managed()
    for token in (
        "**every attempt** (N=1, resume, retry; an earlier FINAL never counts)",
        "Join every delegated writer",
        "`--skip-final-review` → no FINAL and no archive",
        "always a Task subagent, even N=1",
        "Missing or unverifiable evidence → `issues`",
        "If `state` changed during the review, discard the result",
        "`issues` → STOP `E-ARCHIVE-BLOCKED`",
        "The executor MUST NOT write it, and it never waives FINAL",
        "Never `mv`, `cp`, `rename`, or `mkdir` a destination",
        "An existing `.archiving` marker always stops",
        "never reclaim, never infer the owner is dead",
        "--clear-marker <token>",
        "A FINAL pass is not a commit, PR, merge, release or human approval",
    ):
        assert token in m, token
    skill = _impl("SKILL.md")
    assert "archive-blocked" in skill and "**archive-blocked**, not complete" in skill


def test_stale_to_do_path_is_resolved_before_missing_file_check():  # STATIC
    skill, m = _impl("SKILL.md"), _managed()
    pre = skill.index("Managed path-shape pre-check")
    assert pre < skill.index(
        "STOP `E-SOURCE-MISSING` citing the path"
    )  # before the missing-file bullet
    assert "even if it no longer exists" in skill
    assert "This runs **before** the missing-file check" in m
    assert "Neither location exists → `E-SOURCE-MISSING`" in m


def test_managed_location_resolution_order():  # STATIC
    m = _managed()
    rows = [
        line
        for line in m.splitlines()
        if line.startswith(
            (
                "| both exist",
                "| only `<done>`",
                "| `<pkg>/.archiving`",
                "| only `<pkg>`",
            )
        )
    ]
    assert len(rows) == 4 and rows[0].startswith(
        "| both exist"
    )  # conflict checked first
    assert (
        "`E-MANAGED-CONFLICT`" in rows[0] and "Never merge, move, or delete" in rows[0]
    )
    assert "already archived: <actual done path>" in rows[1]
    assert "Never print `already complete` for an unarchived package" in m
    assert "active all-complete" in m and "archive-blocked: <reason>" in m


def test_helper_invocation_uses_skill_base_directory_and_uv_not_repo_path():  # STATIC
    m = _managed()
    cmds = [x for x in m.splitlines() if "archive_workspace.py" in x and "uv run" in x]
    assert cmds
    for line in cmds:
        assert (
            'uv run --no-project python "<skill base>/scripts/archive_workspace.py"'
            in line
        )
        assert "src/superclaude" not in line
        assert "python -m" not in line
    assert "never hardcode a repository `src/` path" in m
    assert (_IMPL / "scripts" / "archive_workspace.py").is_file()


def test_enforcement_map_separates_protocol_from_executable():  # STATIC
    m = _managed()
    assert "## Enforcement map" in m
    assert "**protocol**" in m and "**executable**" in m
    assert "tests/skills/test_workflow_archive.py" in m
    assert "unsupported; not claimed" in m


def test_command_surface_documents_managed_packages():  # STATIC
    cmd = _IMPL_CMD.read_text(encoding="utf-8")
    assert "## Managed workflow packages" in cmd
    assert "Move a package by any means other than the archive helper" in cmd
    assert "Managed packages always use the sibling `progress.md`" in cmd
    assert "blocks archiving" in cmd


def test_managed_ledger_extension_examples_parse_with_the_shipped_helper(
    tmp_path,
):  # CROSS
    ledger = _impl("refs/ledger.md")
    ext = ledger.split("## Managed-package extension", 1)[1].split("## Negative", 1)[0]
    block = next(
        b for b in ext.split("```") if b.lstrip().startswith("# implement ledger")
    )
    f = tmp_path / "progress.md"
    f.write_text(block.lstrip(), encoding="utf-8")
    kinds = [k for k, _, _ in aw._parse_ledger(f)]
    assert kinds == ["header", "plan", "start", "verdict", "final", "archive"]
    # regexes advertised in the doc accept the doc's own example lines (and not junk)
    samples = {
        k: line
        for k, _, line in aw._parse_ledger(f)
        if k in ("plan", "final", "archive")
    }
    for rx in re.findall(r"^\^((?:PLAN|FINAL|ARCHIVE):.*\$)$", ext, re.M):
        name = rx.split(":", 1)[0].lower()
        assert re.match("^" + rx, samples[name]), rx
        assert not re.match("^" + rx, "T1: start sha=" + "0" * 40)
    # legacy examples still satisfy the (unchanged) legacy grammar in the helper
    legacy = re.search(r"Compliant complete:\s+```\n(.+?)\n```", ledger, re.S).group(1)
    assert aw._VERDICT.match(legacy)
    assert not aw._VERDICT.match("Task 1: done")


def test_machine_schema_has_no_inline_comments_and_is_helper_readable():  # CROSS
    gates = (_WF_REFS / "quality-gates.md").read_text(encoding="utf-8")
    block = gates.split("```yaml", 1)[1].split("```", 1)[0]
    assert "#" not in block
    vals = aw._kv(block.replace("<id>", "TASK-WF-x-20261001-063000"))
    assert (
        vals["slug"] == "TASK-WF-x-20261001-063000" and vals["source"] == "./source.md"
    )
    assert vals["created_date"] == "YYYY-MM-DD" and vals["version"] == "1"
    assert "Field rules (outside the machine example" in gates


def test_ownerless_marker_recovery_is_documented_narrowly():  # STATIC
    m = _managed()
    for token in (
        "empty token is rejected",
        "Owner-less marker",
        "non-recursive `rmdir <package>/.archiving`",
        "never `rm -r`",
        "Only after the operator confirms the original run has stopped",
    ):
        assert token in m, token
