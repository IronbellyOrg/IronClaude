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
        "Acceptance never waives FINAL or evidence of current outcomes",
        "Never `mv`, `cp`, `rename`, or `mkdir` a destination",
        "An existing `.archiving` marker always stops",
        "never reclaim, never infer the owner is dead",
        "--clear-marker <token>",
        "A FINAL pass is not a commit, PR, merge, release or human approval",
        "as `refs/qa.md` (Managed FINAL review) defines it",
        "include the package root so `./artifacts/` tokens resolve",
    ):
        assert token in m, token
    skill = _impl("SKILL.md")
    assert "archive-blocked" in skill and "**archive-blocked**, not complete" in skill


def test_managed_final_judges_end_state_not_ledger_line_numbers():  # STATIC
    qa, ledger = _impl("refs/qa.md"), _impl("refs/ledger.md")
    final = qa.split("## Managed FINAL review", 1)[1].split("## Subagent prompt", 1)[0]
    assert "Missing, stale or unverifiable" not in qa
    for token in (
        "not copied from the ledger",
        "the one exception to the Isolation rule above",
        "so a moved line number alone is never `issues`",
        "no evidence for it can be found in the current files or logs",
        "a later change contradicts it",
        "a plan `## Constraints` item is violated",
        "shows a failure at its outcome line",
    ):
        assert token in final, token
    ext = ledger.split("## Managed-package extension", 1)[1].split("## Negative", 1)[0]
    assert "cites the line that shows the outcome" in ext
    assert "not the trailing `rc=` line" in ext
    assert "one token per outcome" in ext


def test_protocol_prose_has_no_cross_file_line_pointers():  # STATIC
    # a "SKILL.md:116"-style pointer goes stale as soon as a later task edits that file
    hits = [
        f"{p.relative_to(_IMPL)}:{n}"
        for p in sorted(_IMPL.rglob("*.md"))
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
        if re.search(r"\b(?:SKILL|qa|ledger|retry|managed-workspace)\.md:\d+", line)
    ]
    assert not hits, hits


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


def test_session_confirmation_contract_and_documented_ruling(
    tmp_path,
):  # STATIC + CROSS
    qa, ledger, managed = _impl("refs/qa.md"), _impl("refs/ledger.md"), _managed()
    assert (
        "clear user confirmation in the current conversation is sufficient"
        in qa.lower()
    )
    assert "MUST automatically append" in qa and "MUST automatically append" in ledger
    assert "missing/ambiguous confirmation" in qa and "STOP `E-NO-RULING`" in qa
    assert "executor-invented approval" in qa and "unchanged" in qa
    assert "Do not ask the user for duplicate archive approval" in managed
    assert "conversation truth" in managed and "**protocol**" in managed
    for doc in (qa, ledger, managed):
        assert "MUST NOT write" not in doc
    example = next(
        line
        for line in ledger.splitlines()
        if line.startswith("T2: Ruling:") and "user confirmed" in line
    )
    assert '"yes, accept T2 as explained"' in example
    path = tmp_path / "progress.md"
    path.write_text(
        "# implement ledger — source: spec.md — created: 2026-10-22T00:00:00Z\n"
        + example
        + "\n",
        encoding="utf-8",
    )
    assert [kind for kind, _, _ in aw._parse_ledger(path)] == ["header", "ruling"]


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


def _fence_lines(text: str):
    """Non-empty lines of every fenced block in ``text``."""
    return [
        line
        for block in text.split("```")[1::2]
        for line in block.strip("\n").splitlines()
        if line
    ]


def test_ledger_retry_halt_examples_parse_with_helper(tmp_path):  # CROSS
    ledger = _impl("refs/ledger.md")
    # grammar blocks carry exactly the helper's regexes
    assert aw._RETRY.pattern in ledger and aw._HALT.pattern in ledger
    examples = ledger.split("## Examples (must match)", 1)[1].split(
        "## Managed-package extension", 1
    )[0]
    header = "# implement ledger — source: ./x.md — created: 2026-10-01T06:30:00Z\n"
    f = tmp_path / "progress.md"
    kinds = []
    for line in _fence_lines(examples):
        f.write_text(header + line + "\n", encoding="utf-8")
        kinds.append(aw._parse_ledger(f)[1][0])
    assert kinds.count("retry") == 3 and kinds.count("halt") == 1
    # the managed example fence parses as written (it starts with its own header)
    ext = ledger.split("## Managed-package extension", 1)[1].split("## Negative", 1)[0]
    block = next(
        b for b in ext.split("```") if b.lstrip().startswith("# implement ledger")
    )
    f.write_text(block.lstrip(), encoding="utf-8")
    assert aw._parse_ledger(f)[0][0] == "header"


def test_corrupt_check_lists_retry_and_halt():  # STATIC
    line = next(
        x
        for x in _impl("refs/ledger.md").splitlines()
        if x.startswith("if last line does not match")
    )
    assert "header|start|verdict|ruling|retry|halt|FINAL" in line
    assert "E-LEDGER-CORRUPT" in line


def _resume_rows():
    ledger = _impl("refs/ledger.md")
    sect = ledger.split("### Per-task resume table", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for m in re.finditer(r"^\| (1|R|P|H|V|X|O|B|S) \| (.+?) \| (.+) \|$", sect, re.M):
        rows[m.group(1)] = (m.group(2), m.group(3))
    order = re.findall(r"^\| (1|R|P|H|V|X|O|B|S) \|", sect, re.M)
    return sect, order, rows


def test_resume_table_row_order_and_text():  # STATIC (wording pin; the rows are prose)
    sect, order, rows = _resume_rows()
    assert order == ["1", "R", "P", "H", "V", "X", "O", "B", "S"]
    assert "no `retry` and no `halt` record" in rows["P"][0]
    assert "Re-run only the review" in rows["V"][1]
    assert "n = 5" in rows["O"][1]
    assert "one `/sc:implement` invocation writes a given ledger at a time" in sect
    assert "there is no lock" in sect
    assert "replaces only the per-task dispatch" in sect
    assert "legacy and managed ledgers alike" in sect
    assert "Ruling eligibility rule in `refs/retry.md`" in sect
    managed = _impl("refs/ledger.md").split("## Managed-package extension", 1)[1]
    assert "first non-complete task → the per-task resume table (Resume)" in managed


def test_row_x_runs_block_as_recheck():  # STATIC (wording pin)
    _, _, rows = _resume_rows()
    x = rows["X"][1]
    assert "Run `sc_retry_revert` directly" in x
    assert "exit 2 maps to the halt" in x
    assert "are the re-check" in x
    # no separate parent re-check before the block (row O is the one that re-checks)
    assert "Re-check" not in x and "re-check the ladder" not in x.lower()
    assert "Re-check" in rows["O"][1]


# Rules (a)-(c): one text in SKILL.md and refs/retry.md (word for word).
_PARALLEL_RULES = (
    "(a) A batch is formed only from tasks that have no `start` line, and it writes "
    "every member's `start` line, in source order, before any member begins Q1; a "
    "member not started by then waits for the next batch. (b) The next task or batch "
    "starts only after every member of the batch has its own `complete` or `halt` "
    "line; a `halt` then STOPs the run (Q8), it never lets the run continue. (c) A "
    "task that already has a `start` line (any resumed task) never joins a batch: it "
    "runs alone, and whether it is a batch task is read from the ledger "
    "(`refs/retry.md`), never from this invocation. A batch task gets no retry "
    "ladder: when A2 fails it halts `batch` (`E-HALT-QA`), and nothing in a batch is "
    "reverted."
)


def test_retry_ref_rules_text():  # STATIC (wording pins only)
    r = _impl("refs/retry.md")
    for heading in (
        "## Attempt ladder (per task)",
        "## Names, paths and ledger records",
        "## When the ladder runs",
        "## Escalation procedure",
        "## The revert",
        "## Sweep refs",
        "## Failed-attempt artifacts",
        "## Halts and transient stops",
    ):
        assert r.count(heading + "\n") == 1, heading
    # parallel rules (a)-(c), word for word
    assert "> " + _PARALLEL_RULES + "\n" in r
    # per-run cap predicate: other tasks with a retry step=open record, never itself
    assert (
        "if at least `RETRY_BUDGET` **other** tasks in this ledger have a "
        "`retry … step=open` record after their latest `start`. T never counts itself."
    ) in r
    assert "`RETRY_BUDGET = 8`" in r
    # the k rule
    assert "k = the last attempt whose review failed" in r
    assert "k = 2 when no such record exists" in r
    assert 'Never "k = number of `blocked` lines"' in r
    assert "k = n - 1" in r
    # names, refs and the Q0 HEAD file
    assert "every `.` replaced by `_2e`" in r
    assert "sweep-<k>-<seq>" in r and "retry/T<rid>/a<k>" in r
    assert "written at Q0, only when the Q0 snapshot is a tree" in r
    # sweep refs: kept at complete, listed in the final summary
    assert (
        "The final summary lists them with one `git update-ref -d <ref>` line "
        "each for the operator."
    ) in r
    assert "keep its sweep refs" in r
    # procedure step 0: the three evidence files are written before the blocked line
    step0 = r.split("0. **Procedure step 0, record the failure.**", 1)[1].split(
        "1. **Procedure step 1", 1
    )[0]
    for name in ("`review-<k>.md`", "`approach-<k>.md`", "`extras-<k>.log`"):
        assert name in step0.split("Then append the existing `blocked`", 1)[0], name
    assert "The order is evidence, then `blocked`." in step0
    # citation-stability rule and the diff cap
    assert (
        'git -C "$top" diff --quiet "$start" <checkpoint tree> -- \':(literal)<path>\''
        in r
    )
    assert "Cap the file at 256 KiB and end a cut file with the line" in r
    # brief layout and the five pick-line forms
    for token in (
        "in one layout for every n:",
        "1. line 1, the pick line;",
        "6. a last line `differs-by: <text>`",
        "`pick: advice-<n>-<x>.md; runner-up: advice-<n>-<y>.md; reason: <a> vs <b> review findings cited`",
        "`…; reason: tie, -a`",
        "`pick: advice-<n>.md; runner-up: none; reason: single adviser`",
        "`pick: advice-<n>-<x>.md; runner-up: none; reason: only passing answer`",
        "`pick: advice-<n>-c.md; runner-up: none; reason: critique adviser`",
        "`pick: refactor of advice-4-<y>.md; runner-up: none; reason: escalation 3`",
    ):
        assert token in r, token
    # recounted cost sentence
    assert (
        "Worst case: 5 reviews instead of 2, and at most 6 adviser spawns "
        "(2 at escalation 1, 2 at escalation 2, plus 2 critiques)."
    ) in r
    # model ladder: both ladder sentences and the four fallback rows, exactly
    assert "The two ladders are never mixed." in r
    assert "never used as an adviser" in r and "`T2_Model01` is on par" in r
    for row in (
        "| `haiku` | 1× `sonnet` | 2× `opus` |",
        "| `sonnet` | 1× `opus` | 2× `opus` |",
        "| `opus` (known) | 2× `opus` (spec requirement) | 2× `opus` |",
        "| unknown | 1× `opus` (so the two escalations still differ) | 2× `opus` |",
    ):
        assert row in r, row
    # Ruling eligibility rule (a)/(b)
    assert "A `T<id>: Ruling:` line is eligible iff (a) a `halt` record follows" in r
    assert "or (b) the task has no `retry` and no `halt` record, the Ruling comes" in r


# --- halt spans and reason lists (protocol files) ----------------------------------
_TRANSIENT = {"reviewer-down", "erase-incomplete", "ref-failed", "adviser-missing"}
_LEDGER_GRAMMAR_LINES = (
    "T<id>: halt review=<2|3|4|5> reason=<reason>",
    "^T([0-9A-Za-z.-]+): halt review=([2-5]) reason=([a-z][a-z-]*)$",
)


def _reason_table():
    """(reason, review value) pairs of the reason-to-`review=` table in refs/retry.md."""
    pairs = []
    for m in re.finditer(
        r"^\| `([a-z][a-z-]*)` \| .+ \| ([2-5](?:, [2-5])*) \|$",
        _impl("refs/retry.md"),
        re.M,
    ):
        pairs += [(m.group(1), int(v)) for v in m.group(2).split(", ")]
    return pairs


def _code_regions(text: str):
    """Fenced blocks and inline code spans of ``text`` (each a string)."""
    fences = re.findall(r"```[^\n]*\n(.*?)```", text, re.S)
    rest = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.S)
    return fences + re.findall(r"`([^`\n]+)`", rest)


def _check_halt_spans(text: str, table, label: str, skip=()):
    """Errors for every halt span in ``text`` that is neither form 1 nor a legal form 2."""
    legal = set(table)
    reasons = {r for r, _ in table}
    for line in skip:
        text = text.replace(line, "")
    errors = []
    for region in _code_regions(text):
        for m in re.finditer(r"halt ([^`\n]*)", region):
            span = m.group(1)
            if span == "review=<k> reason=<r>":
                for reason, value in sorted(table):
                    if not aw._HALT.match(f"T1: halt review={value} reason={reason}"):
                        errors.append(f"{label}: form 1 expansion {reason}/{value}")
                continue
            f2 = re.fullmatch(r"review=([2-5]) reason=([a-z][a-z-]*)", span)
            if not f2 or not aw._HALT.match(f"T1: halt {span}"):
                errors.append(f"{label}: bad halt span `halt {span}`")
            elif (f2.group(2), int(f2.group(1))) not in legal:
                errors.append(f"{label}: pair not in table `halt {span}`")
    # reason tokens bound by "r = `x`" / "r is `x` or `y`" in a line holding a form 1 span
    for line in text.splitlines():
        if "`halt review=<k> reason=<r>`" not in line:
            continue
        for m in re.finditer(
            r"\br (?:=|is) (`[^`\n]+`(?:(?: or |, )`[^`\n]+`)*)", line
        ):
            for tok in re.findall(r"`([^`\n]+)`", m.group(1)):
                if tok not in reasons:
                    errors.append(f"{label}: illegal reason token `{tok}`")
    return errors


def test_retry_ref_and_reason_lists():  # STATIC
    table = _reason_table()
    assert len(table) == 22 and len({r for r, _ in table}) == 11
    for name, skip in (
        ("refs/retry.md", ()),
        ("refs/ledger.md", _LEDGER_GRAMMAR_LINES),
        ("SKILL.md", ()),
    ):
        assert _check_halt_spans(_impl(name), table, name, skip) == [], name
    # the ledger grammar lines are skipped only because they are exactly those lines
    ledger = _impl("refs/ledger.md")
    assert all(line in ledger for line in _LEDGER_GRAMMAR_LINES)
    # transient list is exactly the four reasons; no other E-RESUME-NEEDED reason anywhere
    retry = _impl("refs/retry.md")
    alt = re.search(r"`E-RESUME-NEEDED reason=<([a-z|-]+)>`", retry).group(1)
    assert set(alt.split("|")) == _TRANSIENT and len(alt.split("|")) == 4
    for name in ("refs/retry.md", "refs/ledger.md", "SKILL.md"):
        for tok in re.findall(r"E-RESUME-NEEDED reason=([a-z][a-z-]*)", _impl(name)):
            assert tok in _TRANSIENT, (name, tok)
    # the halt-examples block is exactly the table (22 lines), checked by the helper
    block = re.search(r"```halt-examples\n(.*?)```", retry, re.S).group(1).splitlines()
    assert len(block) == 22
    got = []
    for line in block:
        m = aw._HALT.match(line)
        assert m, line
        got.append((m.group(3), int(m.group(2))))
    assert sorted(got) == sorted(table)
    # Ruling eligibility rule (a)/(b)
    assert (
        "A `T<id>: Ruling:` line is eligible iff (a) a `halt` record follows the "
        "task's latest `blocked` line, the Ruling comes after that `halt`, and no "
        "verdict line lies between that `halt` and the Ruling; or (b) the task has "
        "no `retry` and no `halt` record, the Ruling comes after its latest "
        "`blocked` line, and no verdict line lies between them."
    ) in retry
    # the Q7 loop line carries no lowercase "halt "
    q7 = next(x for x in _impl("SKILL.md").splitlines() if x.startswith("Q7 GATE"))
    assert "halt " not in q7 and "Halt table" in q7


@pytest.mark.parametrize(
    "bad",
    [
        "`halt reason=budget`",  # no review= field
        "`halt review=2 reason=budget|batch`",  # reason alternation
        "`halt review=5 reason=batch`",  # pair not in the table
        "`halt review=6 reason=budget`",  # review out of range
        "```\nT1: halt review=2 reason=Bad Reason\n```",
        "`halt review=<k> reason=<r>` with r = `bogus`",  # illegal reason token
    ],
)
def test_halt_span_negative_fixtures_fail(bad):  # STATIC (fixtures of this test only)
    assert _check_halt_spans(bad, _reason_table(), "fixture")


@pytest.mark.parametrize(
    "good",
    [
        "`halt review=2 reason=budget`",
        "`halt review=<k> reason=<r>` with r = `dispute`",
        "`halt review=<k> reason=<r>`, where r is `no-snapshot` or `head-moved` and k",
        "```\nT1: halt review=4 reason=no-runner-up\n```",
    ],
)
def test_halt_span_positive_fixtures_pass(good):  # STATIC
    assert _check_halt_spans(good, _reason_table(), "fixture") == []


# --- the sc_retry_revert block (static half; behavior is in test_implement_retry_revert.py) ---
def test_retry_ref_revert_block_present():  # STATIC
    blocks = [
        b
        for b in re.findall(r"```bash\n(.*?)```", _impl("refs/retry.md"), re.S)
        if "sc_retry_revert()" in b
    ]
    assert len(blocks) == 1
    b = blocks[0]
    for token in (
        'cat-file -t "$START"',
        "--no-renames",
        ":(literal)",
        "rev-parse --show-toplevel",
    ):
        assert token in b, token
    assert re.search(r"\sdiff -z\s", b) or re.search(r"\s-z\s", b)
    sources = re.findall(r"--source=\S+", b)
    assert sources and all(s == '--source="$START"' for s in sources), sources
    forbidden = re.compile(
        r"\bgit\s+(?:-C\s+\S+\s+)?"
        r"(?:revert|reset|checkout|stash|clean|commit|commit-tree|update-index)\b"
    )
    assert not forbidden.search(b), forbidden.search(b)
    assert "cat-file -p" not in b
    assert not re.search(r"\brm\s+-[A-Za-z]*[rR]", b)
    # every git call runs as git -C ...
    for line in b.splitlines():
        if line.lstrip().startswith("#"):
            continue
        assert not re.search(r"\bgit\b(?!\s+-C\s)", line), line
    # exit 4: the create-only sweep pin failure branch returns 4
    assert re.search(r'update-ref "\$ref" "\$now" ""\s*\|\|\s*\{[^}]*return 4', b)


# --- SKILL.md wiring of the retry ladder ---------------------------------------------
def test_stop_table_lists_e_resume_needed():  # STATIC
    skill = _impl("SKILL.md")
    rows = {
        m.group(1): m.group(0)
        for m in re.finditer(r"^\| `(E-[A-Z-]+)` \|.*\|$", skill, re.M)
    }
    row = rows["E-RESUME-NEEDED"]
    assert row.rstrip().endswith("| Nothing written |")
    assert "refs/retry.md" in row
    halt = rows["E-HALT-QA"]
    assert (
        "A terminal `halt` record (any reason in `refs/retry.md`); no eligible Ruling"
        in halt
    )
    assert "Non-compliant verdict line and `halt` record written" in halt
    codes = next(x for x in skill.splitlines() if x.startswith("No other `E-*` codes"))
    assert "`E-RESUME-NEEDED`" in codes


def test_parallel_rules_identical_in_skill_and_retry_ref():  # STATIC
    skill = _impl("SKILL.md")
    para = next(x for x in skill.splitlines() if x.startswith("Default sequential"))
    # the four existing sentences are kept; only the last sentence became rules (a)-(c)
    assert para.endswith(" " + _PARALLEL_RULES)
    for kept in (
        "Default sequential in source order.",
        "Unmarked = sequential.",
        "If overlap is obvious (`same file`), stay sequential.",
    ):
        assert kept in para
    assert "After a parallel batch, each task still gets" not in skill
    assert "> " + _PARALLEL_RULES + "\n" in _impl("refs/retry.md")


_TOUCHED_RULE = (
    "Touched files = paths this task created or modified via Write, Edit, or Bash "
    "(product paths, not the ledger)."
)


def test_touched_file_rule_unchanged():  # STATIC
    assert _TOUCHED_RULE in _impl("SKILL.md")
    assert _impl("SKILL.md").count("Touched files =") == 1
    # refs/retry.md never defines touched files itself: any line that restates the rule
    # is a pointer that names the Q1 rule by its text (a line number would drift)
    pointer = "the Q1 `Touched files =` rule in `SKILL.md`"
    seen = 0
    for line in _impl("refs/retry.md").splitlines():
        if "created or modified via Write" in line or "Touched files" in line:
            assert pointer in line and "SKILL.md:" not in line, line
            seen += 1
    assert seen == 3  # procedure step 7, fixed exclusion 6, failed-attempt artifacts


def test_skill_retry_wiring_text():  # STATIC
    skill = _impl("SKILL.md")
    assert (
        "Also load `refs/retry.md` when A2 (the Q5 fix pass) still fails review, or "
        "when resume finds a `retry` or `halt` record in the ledger."
    ) in skill
    q0 = skill.split("Q0 START", 1)[1].split("Q1 EXEC", 1)[0]
    assert "write `<retries>/T<id>/q0-head`" in q0
    assert q0.index("q0-head") < q0.index("Write the start line once")
    assert "Only when the snapshot is a tree" in q0
    assert "and the task's checkpoint refs" in q0 and "keep its sweep refs" in q0
    assert (
        "The final summary lists each kept sweep ref with one "
        "`git update-ref -d <ref>` line for the operator."
    ) in q0
    q5 = next(x for x in skill.splitlines() if x.startswith("Q5 FIX"))
    q7 = next(x for x in skill.splitlines() if x.startswith("Q7 GATE"))
    assert "refs/retry.md" in q5 and "refs/retry.md" in q7
    assert "halt " not in q7  # lowercase "halt " would read as a halt span in a fence
    mode = skill.split("### Reviewer mode (no flag)", 1)[1].split("## Loop", 1)[0]
    assert "the first in-flow review of A1 or A2" in mode
    assert "a fresh Task subagent" in mode and "never spawned as `fork`" in mode
    final = skill.split("### Whole-list review", 1)[1].split(
        "**Managed packages.**", 1
    )[0]
    assert "every brief named by a `retry … step=revert` record" in final
    assert "every file in `<retries>/T<id>/`" in final


def test_reviewer_rules_text():  # STATIC
    qa = _impl("refs/qa.md")
    assert (
        "One reviewer per review; never 2+ reviewer agents for the same review. "
        "No Part 2 code-quality ensemble. No `/sc:reflect`. No 6-agent panel."
    ) in qa
    assert "One reviewer vs the brief" not in qa
    # halt table: the terminal-halt row, the E-RESUME-NEEDED row, the Ruling pointer
    assert (
        "| a terminal `halt` (`refs/retry.md`): the ladder did not run after the fix "
        "pass, or it stopped | HALT `E-HALT-QA`."
    ) in qa
    assert "`fix` \\| `ruling` \\| `resume`" in qa
    assert (
        "| `E-RESUME-NEEDED` (`refs/retry.md`) | re-run the same command; do not "
        "write a Ruling | No |"
    ) in qa
    assert "Ruling eligibility rule in `refs/retry.md`" in qa
    # forbidden-read sentence: in the Subagent prompt section, not in Isolation
    isolation = qa.split("## Isolation", 1)[1].split("## Managed FINAL", 1)[0]
    final = qa.split("## Managed FINAL review", 1)[1].split("## Subagent prompt", 1)[0]
    prompt = qa.split("## Subagent prompt", 1)[1]
    sentence = (
        "You are not given an adviser answer, brief, evidence file or troubleshoot "
        "report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, "
        "managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into "
        "either makes the verdict `cannot-verify`."
    )
    assert sentence in prompt and sentence not in isolation and sentence not in final
    named = re.findall(r"`([^`]*(?:retries/|troubleshoot/))`", sentence)
    assert named == [
        ".dev/implement/<slug>/retries/",
        "<pkg>/artifacts/retries/",
        ".dev/troubleshoot/",
    ]
    assert (
        "Once a run switches to subagent mode it stays there; reviews of A3-A5, "
        "re-run reviews and operator reviews are always subagents."
    ) in prompt
    assert "One mode for the rest of the run" not in qa
    # the managed FINAL reads briefs and the retry folder; the forbidden-read rule never applies
    assert "every brief named by a `retry … step=revert` record" in final
    assert "every file in `<retries>/T<id>/`" in final
    assert "never applies to the FINAL" in final
    assert "never spawned as `fork`" in _impl("SKILL.md")


def test_revert_delete_is_guarded_against_symlinked_ancestors():  # STATIC
    retry = _impl("refs/retry.md")
    block = re.findall(r"```bash\n(.*?)```", retry, re.S)
    block = next(b for b in block if "sc_retry_revert()" in b)
    guard = 'elif ! _sc_retry_linked "$top" "$p" && { [ -e "$top/$p" ] || [ -L "$top/$p" ]; }; then'
    assert block.count(guard) == 1
    assert block.index(guard) < block.index('rm -f -- "$top/$p"')
    assert "only when no directory above `p` is a symlink at that moment" in retry
    assert "and something exists at `p`" in retry


def test_adviser_is_bundled_with_the_plugin_and_selected_by_available_type():  # STATIC
    src = _REPO / "src/superclaude/agents/implement-retry-adviser.md"
    plugin = _REPO / "plugins/superclaude/agents/implement-retry-adviser.md"
    assert plugin.is_file() and plugin.read_bytes() == src.read_bytes()
    assert re.search(r"^tools: Read, Grep, Glob$", plugin.read_text(), re.M)
    retry = _impl("refs/retry.md")
    assert "ends in `:implement-retry-adviser`" in retry
    assert "do not guess the plugin prefix" in retry
    # deterministic order: the bare type first, then only this skill's own plugin
    bare = retry.index("(1) `implement-retry-adviser` itself")
    assert bare < retry.index("(2) the plugin-scoped type")
    assert "Never use another plugin's type with that suffix." in retry
