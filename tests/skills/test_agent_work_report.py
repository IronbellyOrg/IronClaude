"""Tests for the agent work report scripts, on recorded data only (never the real orgs).

Run: uv run pytest tests/skills/test_agent_work_report.py -q
"""

import io
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

SCRIPTS = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "skills"
    / "agent-work-report"
    / "scripts"
)
sys.path.insert(0, str(SCRIPTS))

import activity  # noqa: E402
import check  # noqa: E402
import classify  # noqa: E402
import clickup  # noqa: E402
import collect  # noqa: E402
import common  # noqa: E402
import compare  # noqa: E402
import exclude  # noqa: E402
import match  # noqa: E402
import orca_term  # noqa: E402
import page  # noqa: E402
import prefs  # noqa: E402
import render  # noqa: E402
import run as runmod  # noqa: E402
import sessions  # noqa: E402
import waker  # noqa: E402

ME = "clayphi"
U = "https://github.com/IronbellyOrg/Coder/"
RECENT = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
RECENT_MS = str(
    int((datetime.now(timezone.utc) - timedelta(hours=2)).timestamp() * 1000)
)


def item(n, kind="issue", **kw):
    base = {
        "org": "IronbellyOrg",
        "repo": "Coder",
        "kind": kind,
        "number": n,
        "title": f"Item {n}",
        "url": f"{U}{'pull' if kind == 'pr' else 'issues'}/{n}",
        "author": "someone",
        "assignees": [],
        "labels": [],
        "created": f"2026-10-{n:02d}T00:00:00Z",
        "updated": RECENT,
        "comments": 0,
        "draft": None,
        "review_requests": [],
        "closes": [],
        "boards": [],
        "involves_person": False,
    }
    base.update(kw)
    return base


ITEMS = [
    item(1, assignees=[ME]),
    item(2, kind="pr", review_requests=[ME]),
    item(3, kind="pr", author=ME, closes=[f"{U}issues/4"]),
    item(4),
    item(5, author=ME),
    item(6, author=ME, assignees=["ironbelly"]),
    item(7, involves_person=True),
    item(8, labels=["priority:high"]),
    item(
        9,
        boards=[
            {"board": "Coder - Development", "status": "Backlog", "priority": "Urgent"}
        ],
    ),
]
COVERAGE_OK = {
    "repos": [
        {
            "org": "IronbellyOrg",
            "repo": "Coder",
            "items": 9,
            "errors": [],
            "issues_enabled": True,
        }
    ],
    "boards": [],
    "source_errors": [],
}


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setenv("AWR_ROOT", str(tmp_path))
    monkeypatch.setattr(
        runmod, "automation_runs", lambda since: {"read": True, "runs": []}
    )
    monkeypatch.setattr(compare, "lookup_closed", lambda url: None)
    monkeypatch.setattr(waker, "notify", lambda text: "test notice")
    return tmp_path


def new_run(root, items, coverage=COVERAGE_OK, kind="daily", tasks=None, sess=None):
    folder = runmod.open_run(kind)
    (folder / "github-items.json").write_text(json.dumps(items))
    (folder / "coverage.json").write_text(json.dumps(coverage))
    if tasks is not None:
        (folder / "clickup-items.json").write_text(json.dumps(tasks))
        (folder / "clickup-status.json").write_text(
            json.dumps({"read": True, "calls": 1})
        )
    if sess is not None:
        (folder / "sessions.json").write_text(json.dumps(sess))
        (folder / "sessions-status.json").write_text(
            json.dumps({"read": True, "sessions": len(sess), "missing": []})
        )
    exclude.main(folder)  # Step 4b of SKILL.md: between the sessions and match.py
    match.main(folder)
    classify.main(folder)
    return folder


def stub(root, items=ITEMS, coverage=COVERAGE_OK, tasks=None, sess=None):
    f = new_run(root, items, coverage, tasks=tasks, sess=sess)
    compare.main(f)
    render.main(f)
    return f


NOW = "The fix is open and waiting on review."
# Every written part of the item template (templates/item-template.md), as the model fills it.
NOTES = {
    "state": "In progress",
    "next": "Ryan reviews it.",
    "what": "A fix for the login page.",
    "state_text": NOW,
    "done": "- The fix is written and its checks pass.",
    "todo": "- Ryan reviews it.",
    "happened": "- Ryan commented on 2026-11-03.",
    "recommend": "Merge it once Ryan approves.",
    "needs": "N/A",
    "how": "The GitHub timeline since the previous report.",
    "suggested": "Medium",
    "priority_why": "A useful improvement with a defined remainder.",
}
LIKELY = f"[Item 7]({U}issues/7): not yours, because you are only mentioned. Priority: Low (suggested)."


def need(ref, url, title, what="A fix for the login page."):
    """One "Needs you" entry as templates/needs-you-template.md lays it out."""
    return (
        f"### [{ref}]({url}): {title}\n- **What it is:** {what}\n- **Where it stands:** It waits on you.\n"
        f"- **Question:** Merge it?\n"
        f"- **Why this reaches you:** Row 8 of the escalation table: a merge waits on your answer.\n"
        f"- **Low-stakes options:** None.\n"
        f"- **Options:**\n  - **Merge:** It ships today.\n  - **Wait:** It ships later.\n"
        f"- **Recommendation:** Merge it, because its checks pass.\n"
        f"- **If you do not answer:** The merge stays blocked until you answer.\n"
        f"- **Answer on:** [{ref}]({url})\n"
    )


def fill(folder, needs="Nothing new needs you.", status="progressed: it wrote the fix"):
    text = (
        (folder / "overview.md")
        .read_text()
        .replace("{{RF_PLACEHOLDER:needs_you}}", needs)
    )
    text = re.sub(r"<!-- judge each[^\n]*-->\n", "", text)
    text = re.sub(r"<!-- RF_UPDATE:.*?-->\n", "", text)
    text = text.replace("{{RF_PLACEHOLDER:likely_yours}}", LIKELY)
    for slot, value in NOTES.items():
        text = re.sub(r"\{\{RF_PLACEHOLDER:" + slot + r":[^}]+\}\}", value, text)
    text = re.sub(r"\{\{RF_PLACEHOLDER:status:[^}]+\}\}", status, text)
    (folder / "overview.md").write_text(text)


def check_exit(folder, links=False):
    with pytest.raises(SystemExit) as e:
        check.main(folder, links=links)
    return e.value.code, (folder / "script-checks.md").read_text()


def approve(folder):
    """Record a passing script check of the report as it is now and build its page (what Steps 11-12 leave)."""
    h = runmod.sha256(folder / "overview.md")
    rows = "".join(f"| {c} | PASS | ok |\n" for c in runmod.REQUIRED_CHECKS)
    (folder / "script-checks.md").write_text(
        f"| Check | Result | Detail |\n|---|---|---|\n{rows}\noverview sha256: {h}\n"
    )
    if (
        folder / "compare.json"
    ).exists():  # a run the pipeline stubbed, not a bare test run
        page.main(folder)


def close(folder):
    """Close a test run as a delivered report: a daily run is only ever closed with a passing report."""
    if not (folder / "overview.md").exists():
        (folder / "overview.md").write_text(
            "# Your work\n\n## Needs you\n\nNothing new needs you.\n"
        )
    approve(folder)
    runmod.close_run(folder)


def finish(folder):
    fill(folder)
    close(folder)


# Classification: fixed rules only (FR-26)


def test_groups_follow_the_fixed_rules():
    g = classify.classify(ITEMS, ME)
    assert g[f"{U}issues/1"]["group"] == "assigned"
    assert g[f"{U}pull/2"]["group"] == "assigned" and "review" in g[f"{U}pull/2"]["why"]
    assert g[f"{U}pull/3"]["group"] == "owned"
    assert (
        g[f"{U}issues/4"]["group"] == "owned"
        and f"{U}pull/3" in g[f"{U}issues/4"]["why"]
    )
    assert g[f"{U}issues/5"]["group"] == "opened"
    assert g[f"{U}issues/6"]["group"] == "other"
    assert g[f"{U}issues/7"]["group"] == "candidate"
    assert g[f"{U}issues/8"]["group"] == "other"


def test_priority_sources_and_override_wins():
    assert classify.priority(ITEMS[7], {}) == ("High", "from the `priority:high` label")
    assert classify.priority(ITEMS[8], {})[0] == "Urgent"
    assert classify.priority(ITEMS[0], {}) == ("Unset", "none set")
    lvl, src = classify.priority(
        ITEMS[7], {ITEMS[7]["url"]: {"level": "Low", "why": "told the helper"}}
    )
    assert lvl == "Low" and "Clay" in src


def test_scripts_give_the_same_output_twice(root):
    f = stub(root)
    outs = {
        n: (f / n).read_bytes()
        for n in ("classified.json", "compare.json", "snapshot.json", "overview.md")
    }
    classify.main(f)
    compare.main(f)
    (f / "overview.md").unlink()
    render.main(f)
    for n, b in outs.items():
        assert (f / n).read_bytes() == b, n


# Collection (FR-3)


def test_collect_records_a_failed_repo_and_it_reaches_not_checked(root, monkeypatch):
    def fake(*args, **kw):
        if args[:2] == ("repo", "list"):
            return [
                {"name": "Coder", "isArchived": False, "hasIssuesEnabled": True},
                {"name": "Broken", "isArchived": False, "hasIssuesEnabled": False},
            ]
        if args[0] in ("issue", "pr"):
            if "IronbellyOrg/Broken" in args or "IronbellyGroup/Broken" in args:
                raise common.CommandError("HTTP 500")
            return [
                {
                    "number": 1,
                    "title": "t",
                    "author": {"login": ME},
                    "assignees": [],
                    "labels": [],
                    "createdAt": "2026-10-01T00:00:00Z",
                    "updatedAt": "2026-10-02T00:00:00Z",
                    "url": f"https://github.com/{args[3]}/{'pull' if args[0] == 'pr' else 'issues'}/1",
                    "comments": [],
                }
            ]
        if args[:2] == ("project", "list"):
            return {"projects": []}
        return []

    monkeypatch.setattr(collect, "gh_json", fake)
    f = runmod.open_run("daily")
    collect.main(f)
    cov = json.loads((f / "coverage.json").read_text())
    broken = [r for r in cov["repos"] if r["repo"] == "Broken"]
    assert (
        broken
        and broken[0]["errors"] == ["prs: HTTP 500"]
        and not broken[0]["issues_enabled"]
    )
    assert "Broken: prs: HTTP 500" in (f / "run-log.md").read_text()
    match.main(f)
    classify.main(f)
    compare.main(f)
    render.main(f)
    nc = common.section((f / "overview.md").read_text(), "Not checked")
    assert "Broken: prs: HTTP 500" in nc and "Issues are switched off" in nc


# Run lock and run folder (FR-2, FR-18)


def test_second_open_while_active_is_skipped_and_recorded(root):
    runmod.open_run("daily")
    with pytest.raises(SystemExit) as e:
        runmod.open_run("daily")
    assert e.value.code == 3
    assert any(
        "skipped" in p.name for p in (root / ".dev" / "coordinator" / "wakes").iterdir()
    )


def test_stuck_lock_is_replaced_and_raised_in_needs_you(root):
    lock = root / ".dev" / "coordinator" / "run.lock"
    lock.parent.mkdir(parents=True)
    old = (
        datetime.now(timezone.utc) - timedelta(minutes=150)
    ).isoformat()  # past the 120-minute budget
    lock.write_text(json.dumps({"run": "old-run", "kind": "daily", "started": old}))
    f = stub(root)
    assert (
        json.loads((f / "run.json").read_text())["stuck_run_replaced"]["run"]
        == "old-run"
    )
    text = (
        f / "overview.md"
    ).read_text()  # a notice about the helper leads the report; it is not a "Needs you"
    assert (
        "**Stuck run replaced:** old-run never finished." in text.split("\n## ", 1)[0]
    )
    assert "old-run" not in common.section(text, "Needs you")


def test_close_removes_lock_and_marks_complete(root):
    f = new_run(root, ITEMS)
    close(f)
    assert not (root / ".dev" / "coordinator" / "run.lock").exists()
    assert runmod.latest_completed() == f


def test_incomplete_runs_only_since_the_previous_report(root):
    old = new_run(root, ITEMS)  # never closed
    (root / ".dev" / "coordinator" / "run.lock").unlink()
    done = new_run(root, ITEMS)
    close(done)
    f = new_run(root, ITEMS)
    assert not (f / "incomplete-runs.json").exists(), old.name


def test_automation_history_is_read_per_waker_automation(root, monkeypatch):
    monkeypatch.undo()
    monkeypatch.setenv("AWR_ROOT", str(root))
    calls = {
        "automations list": {
            "automations": [
                {"id": "a", "name": "coordinator-morning-wake"},
                {"id": "b", "name": "other"},
            ]
        },
        "automations runs --id a": {
            "runs": [
                {"startedAt": "2026-10-30T12:00:00Z"},
                {"startedAt": "2026-10-20T12:00:00Z"},
            ]
        },
    }
    monkeypatch.setattr(runmod, "orca_result", lambda args: calls[" ".join(args)])
    got = runmod.automation_runs("2026-10-29T00:00:00")
    assert got["read"] and got["runs"] == [
        {"startedAt": "2026-10-30T12:00:00Z", "automation": "coordinator-morning-wake"}
    ]
    calls["automations list"] = {"automations": [{"id": "b", "name": "other"}]}
    assert (
        "no Orca automation named coordinator-" in runmod.automation_runs("")["reason"]
    )
    monkeypatch.setattr(
        runmod,
        "orca_result",
        lambda args: (_ for _ in ()).throw(common.CommandError("down")),
    )
    assert runmod.automation_runs("")["read"] is False


def test_an_item_that_stops_being_yours_leaves_through_closed(root):
    first = stub(root)
    finish(first)
    moved = [dict(i, assignees=["bob"]) if i["number"] == 1 else i for i in ITEMS]
    second = stub(root, moved)
    closed = common.section(
        (second / "overview.md").read_text(), "Closed since the previous report"
    )
    assert f"]({U}issues/1): no longer yours: now other" in closed
    fill(second)
    assert "carry-forward | PASS" in check_exit(second)[1]


def test_needs_you_for_a_closed_item_is_dropped_with_a_note(root, monkeypatch):
    first = stub(root)
    fill(
        first,
        needs=f"### [Coder pull request #3]({U}pull/3): Approve the merge\nAbout [PR 3]({U}pull/3).",
    )
    close(first)
    monkeypatch.setattr(
        compare,
        "lookup_closed",
        lambda url: "merged 2026-10-30" if url.endswith("pull/3") else None,
    )
    second = stub(root, [i for i in ITEMS if i["number"] != 3])
    text = (second / "overview.md").read_text()
    assert "Approve the merge" not in common.section(text, "Needs you")
    assert "question was dropped because the item closed" in common.section(
        text, "Closed since the previous report"
    )
    fill(second)
    assert "needs-you | PASS" in check_exit(second)[1]


def test_action_log_entries_link_run_and_overview(root):
    f = new_run(root, ITEMS)
    runmod.log_action(f, "delivered", "-", "session summary")
    e = json.loads(
        (root / ".dev" / "coordinator" / "action-log.jsonl")
        .read_text()
        .splitlines()[-1]
    )
    assert (
        e["run"] == f.name
        and e["overview"].endswith("overview.md")
        and e["item"] is None
    )


# Compare and carry forward (FR-19)


def test_compare_new_changed_closed_and_carried(root, monkeypatch):
    first = stub(root)
    finish(first)
    changed = [dict(i) for i in ITEMS if i["number"] not in (5, 7)]
    changed[0]["comments"] = 2
    monkeypatch.setattr(
        compare,
        "lookup_closed",
        lambda url: "closed 2026-10-29" if url.endswith("/5") else None,
    )
    second = new_run(root, changed + [item(10, assignees=[ME])])
    compare.main(second)
    c = json.loads((second / "compare.json").read_text())
    assert c["new"] == [f"{U}issues/10"]
    assert c["changed"][f"{U}issues/1"]["comments"] == {"was": 0, "now": 2}
    assert c["closed"][f"{U}issues/5"]["reason"] == "closed 2026-10-29"
    assert f"{U}issues/7" in c["carried"]


def test_lookup_closes_only_on_not_found(monkeypatch):
    for err, want in (
        ("HTTP 404: Not Found", "no longer visible (not found on GitHub)"),
        ("HTTP 401: Bad credentials", None),
        ("timed out", None),
    ):
        monkeypatch.setattr(
            compare,
            "gh_json",
            lambda *a, e=err: (_ for _ in ()).throw(common.CommandError(e)),
        )
        assert compare.lookup_closed(f"{U}issues/1") == want


def test_unread_repo_items_are_carried_rendered_and_closed_later(root, monkeypatch):
    first = stub(root)
    finish(first)
    bad = {
        "repos": [
            {
                "org": "IronbellyOrg",
                "repo": "Coder",
                "items": 0,
                "errors": ["issues: boom"],
            }
        ],
        "boards": [],
        "source_errors": [],
    }
    monkeypatch.setattr(
        compare,
        "lookup_closed",
        lambda url: pytest.fail("must not look up an unread repo"),
    )
    second = stub(root, [], bad)
    c = json.loads((second / "compare.json").read_text())
    assert not c["closed"] and len(c["carried"]) == len(ITEMS)
    work = common.section((second / "overview.md").read_text(), "Your work by priority")
    assert (
        f"]({U}issues/1)" in work
        and "carried: its source was not read this run" in work
    )
    fill(second)
    code, out = check_exit(second)
    assert "carry-forward | PASS" in out
    close(second)
    monkeypatch.setattr(
        compare,
        "lookup_closed",
        lambda url: "closed 2026-10-30" if url.endswith("issues/5") else None,
    )
    third = new_run(root, [i for i in ITEMS if i["number"] != 5])
    compare.main(third)
    c = json.loads((third / "compare.json").read_text())
    assert f"{U}issues/5" in c["closed"] and f"{U}issues/1" not in c["new"]


def test_a_failed_org_read_closes_nothing(root, monkeypatch):
    first = stub(root)
    finish(first)
    dead = {
        "repos": [],
        "boards": [],
        "source_errors": ["IronbellyOrg repo list: HTTP 401: Bad credentials"],
    }
    monkeypatch.setattr(
        compare,
        "lookup_closed",
        lambda url: pytest.fail("must not look up a failed org"),
    )
    second = stub(root, [], dead)
    c = json.loads((second / "compare.json").read_text())
    assert not c["closed"]
    assert "Nothing open is yours" not in (second / "overview.md").read_text()


# Render and check (FR-11, FR-12, FR-14, FR-19)


def test_render_stubs_once_with_model_slots(root):
    f = stub(root)
    text = (f / "overview.md").read_text()
    block = common.entry_blocks(text)[f"{U}issues/1"]
    assert "{{RF_PLACEHOLDER:needs_you}}" in text and block.startswith(
        f"#### [Coder issue #1]({U}issues/1): Item 1\n"
    )
    assert (
        "- **Done, with evidence:**\n  {{RF_PLACEHOLDER:done:IronbellyOrg-Coder-issue-1}}"
        in block
    )
    labels = [
        lbl for lbl in common.item_parts(block) if lbl in dict(common.ITEM_SECTIONS)
    ]
    assert labels == [
        lbl for lbl, _ in common.ITEM_SECTIONS
    ]  # every part of the template, in its order
    assert (
        "| Assigned to you | 2 |" in text and "| Yours without assignment | 2 |" in text
    )
    assert "ClickUp: not read" in text and "### Unset (5)" in text
    with pytest.raises(SystemExit):
        render.main(f)


def test_check_fails_on_placeholders_then_passes_when_filled(root):
    f = stub(root)
    assert check_exit(f)[0] == 1
    fill(f)
    code, out = check_exit(f)
    assert code == 0, out


def test_check_fails_an_item_that_departs_from_the_template(root):
    f = stub(root)
    fill(f)
    text = (f / "overview.md").read_text()
    assert check_exit(f)[0] == 0
    cases = [
        (
            f"- **Current state:** {NOW}",
            "- **Current state:**",
            "'Current state' is empty",
        ),
        (
            "In progress · Suggested Medium",
            "Sort of moving · Suggested Medium",
            "its state 'Sort of moving' is not one of the list",
        ),
        # The priority protocol: an item nothing set a priority on gets a suggested level and the rule for it.
        (
            "In progress · Suggested Medium",
            "In progress · Suggested Soon",
            "its suggested priority 'Suggested Soon' is not",
        ),
        (
            "- **Why this priority:** A useful",
            "- **Why this priority:** a useful",
            "'Why this priority' does not give the rule",
        ),
        (
            f"- **Current state:** {NOW}",
            "- **Current state:** the fix is open.",
            "'Current state' has a line that does not start with a capital",
        ),
        (
            "- **Why this priority:**",
            "- **Why:**",
            "its sections are not the template's",
        ),
        (
            f"#### [Coder issue #1]({U}issues/1): Item 1",
            f"#### Item 1 ([Coder issue #1]({U}issues/1))",
            "its heading is not its linked identifier",
        ),
        ("**Next:** Ryan reviews it.", "**Next:**", "no Next line"),
    ]
    for old, new, why in cases:
        (f / "overview.md").write_text(text.replace(old, new, 1))
        code, out = check_exit(f)
        assert code == 1 and "template | FAIL" in out and why in out, (why, out)


def test_carry_forward_ignores_yesterdays_closed_and_matches_exact_links(
    root, monkeypatch
):
    first = stub(root, ITEMS + [item(12, assignees=[ME])])
    finish(first)
    monkeypatch.setattr(
        compare,
        "lookup_closed",
        lambda url: "closed 2026-10-29" if url.endswith("/2") else None,
    )
    second = stub(
        root, [i for i in ITEMS if i["number"] != 2] + [item(12, assignees=[ME])]
    )
    finish(second)
    third = stub(
        root, [i for i in ITEMS if i["number"] != 2] + [item(12, assignees=[ME])]
    )
    fill(third)
    code, out = check_exit(third)
    assert code == 0, out  # issue 2 closed yesterday is not required today
    text = (third / "overview.md").read_text()
    (third / "overview.md").write_text(text.replace(f"]({U}issues/1)", "](removed)"))
    code, out = check_exit(third)
    assert (
        code == 1 and f"{U}issues/1" in out
    )  # issues/12 present does not hide a dropped issues/1


def test_candidates_must_be_judged(root):
    f = stub(root)
    fill(f)
    text = (f / "overview.md").read_text().replace(LIKELY, "(not judged)")
    (f / "overview.md").write_text(text)
    code, out = check_exit(f)
    assert code == 1 and "candidates | FAIL" in out
    (f / "overview.md").write_text(
        text.replace("(not judged)", "<!-- judge each: x -->" + LIKELY)
    )
    code, out = check_exit(f)
    assert code == 1 and "judge each" in out


def test_every_likely_yours_line_ends_with_a_priority(root):
    # 2026-11-17: nothing goes without a priority, the items that only name Clay included.
    f = stub(root)
    fill(f)
    text = (f / "overview.md").read_text()
    assert "Priority: Low (suggested)." in text
    for bad in (
        LIKELY.replace(" Priority: Low (suggested).", ""),
        LIKELY.replace("Low (suggested)", "Low (set)"),
        LIKELY.replace("Low (suggested)", "Soon (suggested)"),
    ):
        (f / "overview.md").write_text(text.replace(LIKELY, bad))
        code, out = check_exit(f)
        assert code == 1 and "candidates | FAIL" in out and "must end with" in out, bad


def test_a_level_clay_wrote_in_a_comment_counts_as_set(root):
    mine = {
        "by": ME,
        "date": "2026-11-16T12:00:00Z",
        "where": "comment",
        "level": "Low",
        "line": "Parked, low priority.",
    }
    other = {
        "by": "ryan",
        "date": "2026-11-17T12:00:00Z",
        "where": "comment",
        "level": "High",
        "line": "High priority for Leandro.",
    }
    level, src = classify.priority(item(30, priority_mentions=[other, mine]), {})
    assert (level, src) == (
        "Low",
        "a comment by Clay on 2026-11-16",
    )  # only his own word is set by script
    assert classify.priority(item(31, priority_mentions=[other]), {})[0] == "Unset"
    assert (
        classify.priority(
            item(32, labels=["priority:high"], priority_mentions=[mine]), {}
        )[0]
        == "High"
    )  # a label wins
    assert (
        render.priority_why({"priority": level, "priority_source": src})
        == "Low, from a comment by Clay on 2026-11-16."
    )


def test_priority_lines_are_found_but_phase_codes_are_not():
    x = {
        "createdAt": "2026-11-01T00:00:00Z",
        "author": {"login": ME},
        "body": "Rollout in phases P0-P4.\nThis is high priority.",
        "comments": [
            {
                "author": {"login": "ryan"},
                "createdAt": "2026-11-02T00:00:00Z",
                "body": "Set the priority: low\nPriority is Medium now.",
            }
        ],
    }
    got = [(m["by"], m["where"], m["level"]) for m in collect.priority_mentions(x)]
    assert got == [
        (ME, "issue", "High"),
        ("ryan", "comment", "Low"),
        ("ryan", "comment", "Medium"),
    ]


def test_activity_lists_other_peoples_priority_lines_for_every_item_with_none(
    root, monkeypatch
):
    other = {
        "by": "ryan",
        "date": "2026-11-17T12:00:00Z",
        "where": "comment",
        "level": "High",
        "line": "High priority for Leandro.",
    }
    f = new_run(
        root,
        [item(1, assignees=[ME], priority_mentions=[other]), item(2, assignees=[ME])],
    )
    compare.main(f)
    monkeypatch.setattr(activity, "events", lambda url, since: [])
    activity.main(f)
    text = (f / "activity.md").read_text()
    assert (
        "## Priority lines" in text
        and f"({U}issues/1)" in text
        and 'by ryan: "High priority for Leandro."' in text
    )
    assert f"({U}issues/2)" not in text.split("## Priority lines")[1]


def test_dead_links_pass_only_when_marked(root, monkeypatch):
    f = stub(root)
    fill(f)
    monkeypatch.setattr(
        check,
        "run_cmd",
        lambda args, timeout=30: (
            (_ for _ in ()).throw(common.CommandError("404"))
            if args[3].endswith("issues/1")
            else "{}"
        ),
    )
    code, out = check_exit(f, links=True)
    assert code == 1 and "links | FAIL" in out
    text = (
        (f / "overview.md")
        .read_text()
        .replace(f"]({U}issues/1)", f"]({U}issues/1) (dead link)")
    )
    (f / "overview.md").write_text(text)
    code, out = check_exit(f, links=True)
    assert "links | PASS" in out


def test_each_day_starts_from_the_previous_days_text_in_the_template(root):
    first = stub(root)
    fill(first)
    approve(first)  # builds the page and notes.json
    runmod.close_run(first)
    second = stub(
        root
    )  # nothing changed: every item comes back whole, nothing to write
    block = common.entry_blocks((second / "overview.md").read_text())[f"{U}issues/1"]
    assert (
        "RF_PLACEHOLDER" not in block
        and "- **Recommendation:** Merge it once Ryan approves." in block
    )
    assert (
        "- Nothing since the previous report (" in block
    )  # what happened: the script says so
    fill(second)
    assert check_exit(second)[0] == 0
    approve(second)
    runmod.close_run(second)
    third = stub(
        root, [dict(i, comments=2) if i["number"] == 1 else i for i in ITEMS]
    )  # issue 1 changed
    block = common.entry_blocks((third / "overview.md").read_text())[f"{U}issues/1"]
    assert (
        "- **Recommendation:** Merge it once Ryan approves." in block
    )  # updated, not written from nothing
    assert "{{RF_PLACEHOLDER:happened:" in block and common.UPDATE_MARK in block
    assert "update marker" in check_exit(third)[1]


def waiting_run(root, numbers=(3,)):
    """A run whose pull requests each have one agent session (s<n>, branch fix-<n>) that ended on a question."""
    s = [sess(f"s{n}", f"fix-{n}") for n in numbers]
    for one in s:
        one["since_previous_report"]["ends_on_question"] = True
    return stub(root, [item(n, kind="pr", branch=f"fix-{n}") for n in numbers], sess=s)


def ask(n, title):
    """The "Needs you" entry of session s<n>, which works on pull request <n>."""
    return need(
        f"Session s{n}",
        f"orca://session/s{n}",
        title,
        what=f"It works on [Coder pull request #{n}]({U}pull/{n}).",
    )


def test_a_waiting_session_is_carried_until_answered_and_nothing_else_is(root):
    # 2026-11-05: "Needs you" is agent sessions stopped and waiting on Clay; other asks stay in their items.
    first = waiting_run(root)
    fill(
        first,
        needs=ask(3, "Pick the fix")
        + "\n"
        + need("Coder issue #1", f"{U}issues/1", "Review the plan"),
        status="waiting on you: asks which fix",
    )
    close(first)
    second = waiting_run(root)
    needs = common.section((second / "overview.md").read_text(), "Needs you")
    assert (
        "Pick the fix" in needs
        and render.CARRIED_NEEDS_YOU in needs
        and "Review the plan" not in needs
    )
    fill(second, needs="", status="waiting on you: asks which fix")
    assert "needs-you | PASS" in check_exit(second)[1]
    runmod.log_action(
        second, "answer", "orca://session/s3", "from session: the first fix"
    )
    close(second)
    third = waiting_run(root)
    assert "Pick the fix" not in common.section(
        (third / "overview.md").read_text(), "Needs you"
    )


def test_missed_days_are_named_and_weekends_are_not_missed():
    from zoneinfo import ZoneInfo

    tz = ZoneInfo("America/Chicago")
    meta = {
        "previous_completed_run": "20261026T120000Z-daily",
        "started": "2026-10-30T12:00:00+00:00",
    }  # Mon -> Fri
    assert (
        "no report on Tue 2026-10-27, Wed 2026-10-28, Thu 2026-10-29"
        in render.missed(meta, tz)
    )
    assert (
        render.missed(
            {
                "previous_completed_run": "20261029T120000Z-daily",
                "started": "2026-10-30T12:00:00+00:00",
            },
            tz,
        )
        == ""
    )
    friday_to_monday = {
        "previous_completed_run": "20261030T120000Z-daily",
        "started": "2026-11-02T13:00:00+00:00",
    }
    assert render.missed(friday_to_monday, tz) == ""
    thursday_to_monday = {
        "previous_completed_run": "20261029T120000Z-daily",
        "started": "2026-11-02T13:00:00+00:00",
    }
    assert (
        render.missed(thursday_to_monday, tz)
        == "**Missed reports:** no report on Fri 2026-10-30."
    )


def test_no_report_on_weekends(root):
    utc = timezone.utc
    saturday, monday = (
        datetime(2026, 11, 7, 13, 0, tzinfo=utc),
        datetime(2026, 11, 9, 13, 0, tzinfo=utc),
    )
    assert "no report on Saturday" in waker.local_gate("morning", saturday)
    assert "no report on Saturday" in waker.local_gate(
        "check-missed", datetime(2026, 11, 7, 15, 0, tzinfo=utc)
    )
    assert waker.local_gate("morning", monday) is None


# ClickUp (FR-3, FR-11)


def task(tid, name, **kw):
    base = {
        "id": tid,
        "name": name,
        "url": f"https://app.clickup.com/t/{tid}",
        "status": {"status": "to do", "type": "open"},
        "assignees": [],
        "creator": {"id": 7, "username": "ryan"},
        "watchers": [],
        "date_created": RECENT_MS,
        "date_updated": RECENT_MS,
        "tags": [],
        "priority": None,
        "list": {"name": "Ops"},
        "space": {"id": "s1"},
    }
    base.update(kw)
    return base


RAW = {
    "tasks": [
        task(
            "86aaa",
            "Task A",
            assignees=[{"id": 42, "username": "Clay P"}],
            tags=[{"name": "ops"}],
            priority={"priority": "high"},
            text_content=f"see {U}issues/1",
        ),
        task("86bbb", "Task B", creator={"id": 42}),
        task(
            "86ccc",
            "Done but open",
            assignees=[{"id": 42}],
            status={"status": "complete", "type": "done"},
        ),
        task("86ddd", "Someone else's", assignees=[{"id": 9, "username": "someone"}]),
    ]
}


def fake_api(
    monkeypatch, pages=(RAW,), chat=(), updated=None, comments=None, dm_fails=False
):
    """Stand in for the ClickUp API: /v2/user is Clay (id 42), one workspace (900), task pages as given.
    `updated` is the task ids updated since the previous report (default: all); `comments` maps a task id to
    its comment pages."""
    calls = []

    def call(method, path, body=None):
        calls.append((method, path))
        if path == "/v2/user":
            return {"user": {"id": 42}}
        if path == "/v2/team":
            return {
                "teams": [
                    {
                        "id": "900",
                        "members": [{"user": {"id": 9, "username": "someone"}}],
                    }
                ]
            }
        if path.startswith("/v2/team/900/task"):
            page = int(path.rsplit("page=", 1)[1])
            if "date_updated_gt" in path:
                return {
                    "tasks": [
                        t
                        for p in pages
                        for t in p["tasks"]
                        if updated is None or t["id"] in updated
                    ],
                    "last_page": True,
                }
            return dict(pages[page], last_page=page == len(pages) - 1)
        if path.startswith("/v2/team/900/space"):
            return {"spaces": [{"id": "s1", "name": "Ironbelly"}]}
        if path.startswith("/v2/task/") and path.split("?")[0].endswith("/comment"):
            tid = path.split("/")[3]
            got = (comments or {}).get(tid, [[]])
            return {"comments": got[1] if "start=" in path and len(got) > 1 else got[0]}
        if path.startswith("/v2/comment/"):
            return {"comments": []}
        if "/chat/channels?" in path:
            return {"data": list(chat)}
        if path.endswith("/direct_message"):
            return {"data": {"id": "dm1"}}
        if "/messages" in path and method == "POST":
            return {"data": {"id": "m1"}}
        if "/messages" in path:
            if dm_fails:
                raise clickup.ClickUpError(
                    "GET /v3/workspaces/900/chat/channels/dm1/messages: HTTP 500"
                )
            return {
                "data": [
                    {"date": "1893430000000", "content": "approve the merge"},
                    {
                        "date": "1893430000000",
                        "content": "# Today's work report: Friday",
                    },
                ]
            }
        raise AssertionError(path)

    monkeypatch.setattr(clickup, "call", call)
    return calls


def test_clickup_needs_a_token_and_never_guesses(root, monkeypatch):
    monkeypatch.delenv("CLICKUP_API_TOKEN", raising=False)
    f = runmod.open_run("daily")
    clickup.main(f)
    st = json.loads((f / "clickup-status.json").read_text())
    assert st["read"] is False and "CLICKUP_API_TOKEN is not set" in st["reason"]
    assert not (f / "clickup-items.json").exists()


def test_clickup_reads_every_page_and_keeps_only_clays_open_work(root, monkeypatch):
    calls = fake_api(
        monkeypatch, pages=({"tasks": RAW["tasks"][:1]}, {"tasks": RAW["tasks"][1:]})
    )
    f = runmod.open_run("daily")
    clickup.main(f)
    assert (
        "GET",
        "/v2/team/900/task?include_closed=false&subtasks=true&page=1",
    ) in calls
    got = {t["number"]: t for t in json.loads((f / "clickup-items.json").read_text())}
    assert sorted(got) == [
        "86aaa",
        "86bbb",
    ]  # a "done" status is finished; someone else's task is not his
    assert got["86aaa"]["location"] == "Ironbelly / Ops" and got["86aaa"][
        "github_links"
    ] == [f"{U}issues/1"]
    gone = json.loads((f / "clickup-gone.json").read_text())
    assert gone["https://app.clickup.com/t/86ccc"].startswith("marked complete")


def test_clickup_lists_only_tasks_active_in_30_days_and_counts_the_rest(
    root, monkeypatch
):
    old = str(int((datetime.now(timezone.utc) - timedelta(days=45)).timestamp() * 1000))
    raw = {
        "tasks": RAW["tasks"]
        + [task("86qqq", "Quiet", assignees=[{"id": 42}], date_updated=old)]
    }
    fake_api(monkeypatch, pages=(raw,), updated={"86aaa", "86bbb"})
    first = runmod.open_run("daily")
    clickup.main(first)
    assert "86qqq" not in {
        t["number"] for t in json.loads((first / "clickup-items.json").read_text())
    }
    assert json.loads((first / "clickup-status.json").read_text())["parts"][
        "quiet"
    ] == {"count": 1, "days": 30}
    (first / "github-items.json").write_text("[]")
    (first / "coverage.json").write_text(json.dumps(COVERAGE_OK))
    for step in (match, classify, compare, render):
        step.main(first)
    assert (
        "1 more ClickUp tasks are assigned to or created by you but had no activity in 30 days"
        in (first / "overview.md").read_text()
    )


def test_tasks_that_went_quiet_leave_as_one_count_line(root):
    first = stub(root, [], tasks=[cu("86q1"), cu("86q2"), cu("86aaa")])
    finish(first)
    second = runmod.open_run("daily")
    for name, data in (
        ("github-items.json", []),
        ("coverage.json", COVERAGE_OK),
        ("clickup-items.json", [cu("86aaa")]),
        (
            "clickup-status.json",
            {"read": True, "calls": 1, "parts": {"quiet": {"count": 2, "days": 30}}},
        ),
        (
            "clickup-gone.json",
            {
                f"https://app.clickup.com/t/86q{i}": f"{common.QUIET_REASON} 30 days"
                for i in (1, 2)
            },
        ),
    ):
        (second / name).write_text(json.dumps(data))
    for step in (match, classify, compare, render):
        step.main(second)
    closed = common.section(
        (second / "overview.md").read_text(), "Closed since the previous report"
    )
    assert (
        "86q1" not in closed
        and "- 2 ClickUp tasks left the list: still open, but nothing happened on them in 30 days"
        in closed
    )
    fill(second)
    assert "carry-forward | PASS" in check_exit(second)[1]


def test_clickup_dm_and_replies(root, monkeypatch):
    fake_api(monkeypatch)
    assert clickup.send_dm("hello") == (True, "dm1")
    assert (
        json.loads((root / ".dev" / "coordinator" / "settings.json").read_text())[
            "clickup_dm_channel"
        ]
        == "dm1"
    )
    f = runmod.open_run("daily")
    clickup.main(f)
    assert [
        r["text"] for r in json.loads((f / "clickup-replies.json").read_text())
    ] == ["approve the merge"]


def test_clickup_tasks_flow_through_classify_render_and_check(root, monkeypatch):
    fake_api(monkeypatch)
    f = runmod.open_run("daily")
    clickup.main(f)
    tasks = {t["url"]: t for t in json.loads((f / "clickup-items.json").read_text())}
    assert tasks["https://app.clickup.com/t/86aaa"]["assignees"] == [ME]
    assert tasks["https://app.clickup.com/t/86bbb"]["author"] == ME
    (f / "github-items.json").write_text("[]")
    (f / "coverage.json").write_text(json.dumps(COVERAGE_OK))
    match.main(f)
    classify.main(f)
    cls = json.loads((f / "classified.json").read_text())["items"]
    assert cls["https://app.clickup.com/t/86aaa"]["group"] == "assigned"
    assert cls["https://app.clickup.com/t/86aaa"]["priority"] == "High"
    compare.main(f)
    render.main(f)
    text = (f / "overview.md").read_text()
    assert (
        "{{RF_PLACEHOLDER:what:clickup-task-86aaa}}" in text
        and "ClickUp task 86aaa" in text
    )
    assert (
        "#### [ClickUp task 86aaa](https://app.clickup.com/t/86aaa): Task A\n" in text
    )
    assert (
        "**Assigned to:** clayphi · **Owner:** You (assigned to you) · **Board:** ClickUp status: to do"
        in text
    )
    fill(f)
    code, out = check_exit(f)
    assert code == 0 and "template | PASS" in out


def test_clickup_chat_names_the_sender_and_is_not_a_needs_you_entry(root, monkeypatch):
    chat = [{"id": "c1", "type": "DM"}]
    fake_api(monkeypatch, chat=chat)
    monkeypatch.setattr(
        clickup,
        "read_channel",
        lambda team, ch, since, me, tag: [
            {
                "channel": "c1",
                "channel_type": "DM",
                "from_user_id": 9,
                "date": RECENT,
                "text": "can you review this?",
                "mentions_you": False,
                "github_links": [],
            }
        ],
    )
    f = runmod.open_run("daily")
    clickup.main(f)
    (f / "github-items.json").write_text("[]")
    (f / "coverage.json").write_text(json.dumps(COVERAGE_OK))
    for step in (match, classify, compare, activity, render):
        step.main(f)
    assert 'from someone: "can you review this?"' in (f / "activity.md").read_text()
    assert (
        "consider for Needs you" not in (f / "overview.md").read_text()
    )  # Needs you is waiting sessions only


# Activity (commit times)


def test_activity_keeps_commits_after_the_previous_report(monkeypatch):
    page = [
        [
            {
                "event": "committed",
                "sha": "abcdef1234",
                "message": "fix x",
                "author": {"date": "2026-10-30T10:00:00Z"},
            },
            {
                "event": "commented",
                "actor": {"login": "bob"},
                "body": "hi",
                "created_at": "2026-10-30T10:05:00Z",
            },
            {
                "event": "commented",
                "actor": {"login": "old"},
                "body": "before",
                "created_at": "2026-10-20T10:05:00Z",
            },
            {
                "event": "referenced",
                "actor": {"login": "ann"},
                "commit_id": "9988776655",
                "created_at": "2026-10-30T11:00:00Z",
            },
        ]
    ]
    monkeypatch.setattr(activity, "gh_json", lambda *a: page)
    lines = activity.events(f"{U}pull/3", "2026-10-29T00:00:00")
    assert any("commit abcdef12" in ln for ln in lines) and not any(
        "before" in ln for ln in lines
    )
    assert any(
        "a commit by ann mentioned this item in its message (commit 99887766)" in ln
        for ln in lines
    )


# Recording what Clay says (FR-17, FR-20)


def test_prefs_reads_words_from_stdin_and_validates(root, monkeypatch):
    f = new_run(root, ITEMS)
    monkeypatch.setattr(sys, "stdin", io.StringIO('it\'s "urgent" $(rm -rf /)'))
    prefs.set_priority(f, f"{U}issues/1", "High")
    p = json.loads((root / ".dev" / "coordinator" / "priorities.json").read_text())
    assert p[f"{U}issues/1"] == {"level": "High", "why": 'it\'s "urgent" $(rm -rf /)'}
    for bad in (
        lambda: prefs.set_priority(f, "not a url", "High"),
        lambda: prefs.set_priority(f, f"{U}issues/1", "Top"),
    ):
        monkeypatch.setattr(sys, "stdin", io.StringIO("x"))
        with pytest.raises(SystemExit):
            bad()
    monkeypatch.setattr(sys, "stdin", io.StringIO("approve it"))
    prefs.record_answer(f, f"{U}issues/1", "clickup-dm")
    assert common.answered_since("") == {f"{U}issues/1"}


# Terminal and waker (FR-25)


def test_truncated_terminal_list_is_an_error(monkeypatch):
    monkeypatch.setattr(
        orca_term,
        "orca",
        lambda *a, **k: {"terminals": [], "truncated": True, "totalCount": 500},
    )
    with pytest.raises(common.CommandError):
        orca_term.terminals("/w")


def test_terminal_results_are_read_from_orcas_real_shapes(monkeypatch):
    # Shapes recorded from Orca CLI 1.4.237 on 2026-10-30 (screen read) and the proof run (send receipt).
    shapes = {
        "read": {
            "terminal": {
                "handle": "h",
                "status": "running",
                "tail": ["a", "Session name (Enter = untagged...):"],
                "draft": "half typed",
                "source": "screen",
            }
        },
        "send": {
            "send": {
                "handle": "h",
                "accepted": True,
                "stages": ["input_accepted", "turn_started"],
            }
        },
        "wait": {"wait": {"satisfied": True}},
    }
    monkeypatch.setattr(orca_term, "orca", lambda *a, **k: shapes[a[1]])
    s = orca_term.screen("h")
    assert s["draft"] == "half typed" and s["tail"][-1].startswith("Session name")
    assert orca_term.send("h", "x")["stages"] == ["input_accepted", "turn_started"]
    assert orca_term.is_idle("h") is True
    term_ = {"handle": "h", "lastOutputAt": 0}
    assert "typing" in orca_term.typing_or_fresh(term_)


class FakeOrca:
    """The workspace's terminals and the Claude processes in them. A terminal in `live` runs Claude under the
    coordinator tag; `prompt` terminals sit at ccsession's name question. Typing a tag starts Claude there."""

    def __init__(
        self,
        terms,
        draft="",
        idle=True,
        stages=("input_accepted", "turn_started"),
        live=None,
        prompt=(),
        opens_on_wake=1,
        tail=(),
    ):
        self.terms, self.draft, self.idle, self.stages, self.sent = (
            terms,
            draft,
            idle,
            list(stages),
            [],
        )
        self.live = {
            h: "coordinator"
            for h in (live if live is not None else [t["handle"] for t in terms])
        }
        self.prompt, self.created = set(prompt), []
        # The session opens its run folder when it gets its Nth wake line (None: it never does); `tail` is what
        # its screen shows, for example an API error.
        self.opens_on_wake, self.wakes, self.tail = opens_on_wake, 0, list(tail)

    def send(self, h, text, **kw):
        self.sent.append(text)
        if text in ("coordinator", "ccsession coordinator"):
            self.live[h] = "coordinator"
        if text == waker.WAKE_LINES["morning"]:
            self.wakes += 1
            if self.opens_on_wake and self.wakes >= self.opens_on_wake:
                d = (
                    common.runs_dir()
                    / f"fake-daily-{self.wakes}-{datetime.now().timestamp()}"
                )
                d.mkdir()
                (d / "run.json").write_text(
                    json.dumps(
                        {
                            "kind": "daily",
                            "started": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                )
        return {"stages": self.stages}

    def orca(self, *args, **kw):
        assert args[:2] == ("terminal", "create"), args
        self.created.append("term_new")
        self.terms.append({"handle": "term_new", "connected": True, "lastOutputAt": 0})
        self.prompt.add(
            "term_new"
        )  # a new workspace shell opens with ccsession's name question
        return {"terminal": {"handle": "term_new"}}

    def install(self, monkeypatch):
        monkeypatch.setattr(waker.orca_term, "terminals", lambda w: self.terms)
        monkeypatch.setattr(
            waker.orca_term, "claude_processes", lambda: dict(self.live)
        )
        monkeypatch.setattr(waker.orca_term, "orca", self.orca)
        monkeypatch.setattr(
            waker.orca_term,
            "screen",
            lambda h: {
                "draft": self.draft,
                "tail": ["Session name (Enter = untagged, Ctrl+C = plain shell):"]
                if h in self.prompt
                else self.tail,
            },
        )
        monkeypatch.setattr(waker, "RUN_WAIT_S", 0)
        monkeypatch.setattr(
            waker.orca_term, "is_idle", lambda h, wait_ms=4000: self.idle
        )
        monkeypatch.setattr(waker.orca_term, "send", self.send)
        monkeypatch.setattr(waker.time, "sleep", lambda s: None)
        monkeypatch.setattr(waker, "HOLD_WAIT_S", 0)
        monkeypatch.setattr(waker, "HOLD_RETRIES", 2)
        monkeypatch.setattr(waker, "local_gate", lambda mode, now=None: None)


def term(age_s=600, handle="term_x"):
    return {
        "handle": handle,
        "connected": True,
        "lastOutputAt": (datetime.now().timestamp() - age_s) * 1000,
    }


def last_wake(root):
    return json.loads(
        sorted((root / ".dev" / "coordinator" / "wakes").glob("*.json"))[-1].read_text()
    )


def test_waker_clears_the_session_then_sends_one_line_when_idle(root, monkeypatch):
    o = FakeOrca([term()])
    o.install(monkeypatch)
    waker.wake("morning")
    assert o.sent == ["/clear", waker.WAKE_LINES["morning"]] and last_wake(root)[
        "outcome"
    ].startswith("SENT")


@pytest.mark.parametrize(
    "fake,why",
    [
        (lambda: FakeOrca([term()], draft="half a sentence"), "typing"),
        (lambda: FakeOrca([term(age_s=5)]), "busy or someone was typing"),
        (lambda: FakeOrca([term()], idle=False), "busy"),
    ],
)
def test_waker_holds_back_retries_then_asks_for_a_dm(root, monkeypatch, fake, why):
    o = fake()
    o.install(monkeypatch)
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        o.sent == [] and rec["attempts"] == 2 and rec["outcome"].startswith("DM_NEEDED")
    )
    assert (
        len(list((root / ".dev" / "coordinator" / "wakes").glob("*.json"))) == 1
    )  # one record, rewritten per attempt


def test_a_missed_turn_start_counts_as_sent_once_the_run_opens(root, monkeypatch):
    # 2026-11-04: after /clear Orca reported only "input_accepted", the report ran, and Clay got a false DM.
    o = FakeOrca([term()], stages=("input_accepted",), opens_on_wake=None)
    o.install(monkeypatch)
    waker.wake("morning")
    assert last_wake(root)["outcome"].startswith(
        "DM_NEEDED: the wake line was sent but the session did not start"
    )
    o.opens_on_wake = 1
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        rec["outcome"] == "SENT: input_accepted, run_opened" and "notified" not in rec
    )


API_ERROR = "API Error: Request rejected (429) \N{MIDDLE DOT} ccsession: all Tier 1b models are out of usage; next retry at 13:05"


def test_a_wake_the_session_took_but_never_ran_is_sent_again_then_reported_with_the_error(
    root, monkeypatch
):
    # 2026-11-18: Orca reported turn_started, the session's first request failed with a 429, nothing retried it,
    # and the report never ran; the waker had recorded SENT.
    o = FakeOrca([term()], opens_on_wake=None, tail=["", API_ERROR])
    o.install(monkeypatch)
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        o.sent == ["/clear", waker.WAKE_LINES["morning"]] * 2 and rec["attempts"] == 2
    )  # sent again on the retry
    assert rec["outcome"].startswith(
        "DM_NEEDED: today's report did not start after 2 tries"
    )
    assert (
        "429" in rec["outcome"] and "429" in rec["session_error"] and "notified" in rec
    )


def test_a_retried_wake_that_then_opens_the_run_is_sent(root, monkeypatch):
    o = FakeOrca([term()], opens_on_wake=2, tail=[API_ERROR])
    o.install(monkeypatch)
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        rec["outcome"] == "SENT: input_accepted, turn_started"
        and rec["attempts"] == 2
        and "session_error" not in rec
    )
    assert o.wakes == 2


def test_the_missed_report_message_says_what_the_morning_left_behind(root, monkeypatch):
    told = []
    monkeypatch.setattr(
        waker, "notify", lambda text: told.append(text) or "ClickUp DM sent"
    )
    o = FakeOrca([term()], tail=[API_ERROR])
    o.install(monkeypatch)
    waker.record(
        {
            "mode": "morning",
            "outcome": "DM_NEEDED: today's report did not start after 2 tries over 4 minutes; "
            "the last one ended: the session took the wake line but no report run opened",
            "session_error": API_ERROR,
        }
    )
    waker.check_missed()
    assert (
        "the 7 AM wake ended: DM_NEEDED: today's report did not start" in told[-1]
        and "429" in told[-1]
    )
    for p in (root / ".dev" / "coordinator" / "wakes").glob("*-morning.json"):
        p.unlink()
    waker.check_missed()
    assert (
        "no wake line was sent this morning" in told[-1] and "429" in told[-1]
    )  # the live screen still says why
    d = common.runs_dir() / "fake-daily-open"
    d.mkdir()
    (d / "run.json").write_text(
        json.dumps({"kind": "daily", "started": datetime.now(timezone.utc).isoformat()})
    )
    waker.check_missed()
    assert "fake-daily-open opened but has not finished" in told[-1]


def test_waker_finds_the_session_by_its_process_not_its_title(root, monkeypatch):
    # 2026-11-03: a terminal back at ccsession's name question kept the title "coordinator · Claude Code",
    # and the old title lookup counted two sessions and sent nothing.
    stale, real = term(handle="term_stale"), term(age_s=900, handle="term_real")
    o = FakeOrca([stale, real], live=["term_real"])
    o.install(monkeypatch)
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        rec["outcome"].startswith("SENT")
        and rec["handle"] == "term_real"
        and o.sent == ["/clear", waker.WAKE_LINES["morning"]]
    )


def test_waker_starts_a_missing_session_in_a_spare_terminal_or_a_new_one(
    root, monkeypatch
):
    o = FakeOrca([term(handle="term_shell")], live=[], prompt={"term_shell"})
    o.install(monkeypatch)
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        rec["outcome"].startswith("SENT")
        and rec["started"]
        and rec["handle"] == "term_shell"
        and not o.created
    )
    assert o.sent == [
        "coordinator",
        "/clear",
        waker.WAKE_LINES["morning"],
    ]  # answers the name question, clears, wakes
    o = FakeOrca([], live=[])
    o.install(monkeypatch)
    waker.wake("morning")
    assert last_wake(root)["outcome"].startswith("SENT") and o.created == ["term_new"]


def test_waker_reports_a_session_that_never_starts(root, monkeypatch):
    o = FakeOrca([], live=[])
    o.install(monkeypatch)
    monkeypatch.setattr(
        o, "send", lambda h, text, **kw: o.sent.append(text) or {"stages": []}
    )  # Claude never starts
    monkeypatch.setattr(waker.orca_term, "send", o.send)
    monkeypatch.setattr(waker, "START_WAIT_S", 0)
    waker.wake("morning")
    assert "Claude was not running there" in last_wake(root)["outcome"]


def test_waker_picks_the_newest_of_two_live_sessions_and_still_wakes_past_a_stuck_run(
    root, monkeypatch
):
    FakeOrca(
        [term(age_s=3000, handle="term_old"), term(age_s=900, handle="term_new")]
    ).install(monkeypatch)
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        rec["handle"] == "term_new"
        and rec["other_live_sessions"] == ["term_old"]
        and rec["outcome"].startswith("SENT")
    )
    lock = root / ".dev" / "coordinator" / "run.lock"
    lock.write_text(
        json.dumps(
            {
                "run": "r",
                "kind": "daily",
                "started": (
                    datetime.now(timezone.utc) - timedelta(hours=3)
                ).isoformat(),
            }
        )
    )
    o = FakeOrca([term()])
    o.install(monkeypatch)
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        o.sent
        and rec["outcome"].startswith("DM_NEEDED")
        and "wake sent" in rec["outcome"]
    )


def test_waker_hourly_does_nothing_before_the_coordinator_exists(root, monkeypatch):
    monkeypatch.setattr(waker, "COORDINATOR_BUILT", False)
    waker.wake("hourly")
    assert last_wake(root)["outcome"].startswith("SKIPPED")


def test_local_gate_keeps_only_the_firing_at_local_time(root):
    utc = timezone.utc
    # 12:00 UTC is 07:00 in Chicago during daylight time, 06:00 after the clock change.
    assert (
        waker.local_gate("morning", datetime(2026, 10, 30, 12, 0, tzinfo=utc)) is None
    )
    assert "too early" in waker.local_gate(
        "morning", datetime(2026, 11, 2, 12, 0, tzinfo=utc)
    )
    assert waker.local_gate("morning", datetime(2026, 11, 2, 13, 0, tzinfo=utc)) is None
    f = new_run(root, ITEMS)
    started = datetime.fromisoformat(
        json.loads((f / "run.json").read_text())["started"]
    )
    assert "already started" in waker.local_gate(
        "morning", started + timedelta(hours=1)
    )
    assert (
        waker.local_gate("check-missed", datetime(2026, 10, 30, 14, 0, tzinfo=utc))
        is None
    )
    assert waker.local_gate("check-missed", datetime(2026, 10, 30, 15, 0, tzinfo=utc))


def test_check_missed(root, monkeypatch):
    monkeypatch.setattr(waker, "local_gate", lambda mode, now=None: None)
    waker.check_missed()
    assert last_wake(root)["outcome"].startswith("DM_NEEDED")
    f = new_run(root, ITEMS)
    close(f)
    waker.check_missed()
    assert last_wake(root)["outcome"].startswith("OK")


# Agent sessions from transcripts (FR-27)


def line(kind, ts, content, **kw):
    return json.dumps(
        dict(
            {
                "type": kind,
                "timestamp": ts,
                "message": {"role": kind, "content": content},
            },
            **kw,
        )
    )


def transcript(path, t0):
    ts = [(t0 + timedelta(minutes=i)).isoformat() for i in range(5)]
    path.write_text(
        "\n".join(
            [
                line("user", ts[0], f"fix the login bug in {U}issues/1"),
                line(
                    "assistant",
                    ts[1],
                    [
                        {"type": "text", "text": "Writing the fix."},
                        {
                            "type": "tool_use",
                            "id": "a",
                            "name": "Write",
                            "input": {
                                "file_path": "/w/login.py",
                                "content": f"# like {U}issues/9",
                            },
                        },
                    ],
                ),
                line(
                    "user",
                    ts[2],
                    [{"type": "tool_result", "tool_use_id": "a", "content": "ok"}],
                ),
                line(
                    "assistant",
                    ts[3],
                    [
                        {
                            "type": "tool_use",
                            "id": "b",
                            "name": "Bash",
                            "input": {"command": "git commit -m fix"},
                        }
                    ],
                ),
                json.dumps({"type": "ai-title", "aiTitle": "Fix login"}),
            ]
        )
        + "\n"
    )


@pytest.fixture
def orca_sessions(root, tmp_path, monkeypatch):
    """One Claude terminal with a transcript, one plain shell, one terminal in the coordinator's own workspace."""
    proj = tmp_path / "projects" / "p"
    proj.mkdir(parents=True)
    transcript(proj / "s1.jsonl", datetime.now(timezone.utc) - timedelta(hours=1))
    hook = tmp_path / "last-status.json"
    hook.write_text(
        json.dumps(
            {
                "version": 2,
                "entries": {
                    "t1:l1": {
                        "providerSession": {
                            "id": "s1",
                            "transcriptPath": str(proj / "s1.jsonl"),
                        },
                        "hasExplicitPrompt": True,
                    },
                    "t3:l3": {
                        "providerSession": {
                            "id": "s3",
                            "transcriptPath": str(proj / "s3.jsonl"),
                        },
                        "hasExplicitPrompt": True,
                    },
                },
            }
        )
    )
    terms = [
        {
            "handle": "h1",
            "tabId": "t1",
            "leafId": "l1",
            "worktreePath": "/w",
            "branch": "refs/heads/1-login",
            "connected": True,
        },
        {
            "handle": "h2",
            "tabId": "t2",
            "leafId": "l2",
            "worktreePath": "/w",
            "connected": True,
        },
        {
            "handle": "h3",
            "tabId": "t3",
            "leafId": "l3",
            "worktreePath": common.workspace_path(),
            "connected": True,
        },
    ]
    state = {"terminals": terms}
    monkeypatch.setattr(sessions, "HOOK_FILE", hook)
    monkeypatch.setattr(sessions, "PROJECTS", tmp_path / "projects")
    monkeypatch.setattr(sessions, "claude_processes", lambda: {"h1": ""})
    monkeypatch.setattr(sessions, "git_repo", lambda p: "IronbellyOrg/Coder")
    monkeypatch.setattr(
        sessions.orca_term,
        "orca",
        lambda *a, **k: (
            {"terminals": state["terminals"]}
            if a[0] == "terminal"
            else {"worktrees": [{"path": "/w", "linkedIssue": None, "linkedPR": None}]}
        ),
    )
    return state, proj / "s1.jsonl"


def test_sessions_match_terminals_to_transcripts_and_extract_events(orca_sessions):
    state, path = orca_sessions
    f = runmod.open_run("daily")
    sessions.main(f)
    got = json.loads((f / "sessions.json").read_text())
    assert [s["session_id"] for s in got] == [
        "s1"
    ]  # the plain shell and the coordinator's own terminal are skipped
    s = got[0]
    x = s["since_previous_report"]
    assert (
        s["branch"] == "1-login"
        and s["repo"] == "IronbellyOrg/Coder"
        and s["title"] == "Fix login"
    )
    assert (
        x["events"] == 4
        and x["files_written"] == ["/w/login.py"]
        and x["commands"] == ["git commit -m fix"]
    )
    assert x["pending_tool_call"]["tool"] == "Bash" and not x["ends_on_question"]
    assert x["prompts"][0]["text"].startswith("fix the login bug") and x[
        "prompt_urls"
    ] == [f"{U}issues/1"]
    assert x["item_urls"] == [
        f"{U}issues/1",
        f"{U}issues/9",
    ]  # only the prompt's item can match the session
    assert s["read_offset"] == path.stat().st_size


def test_a_closed_session_stays_until_a_report_calls_it_done(root, orca_sessions):
    state, path = orca_sessions
    first = runmod.open_run("daily")
    sessions.main(first)
    (first / "overview.md").write_text(
        "- **Agent session:** [Fix login](orca://session/s1) · x · status: progressed: wrote it\n"
    )
    close(first)
    state["terminals"] = []  # its terminal was closed
    second = runmod.open_run("daily")
    sessions.main(second)
    s = json.loads((second / "sessions.json").read_text())
    assert [x["session_id"] for x in s] == ["s1"] and s[0]["terminal_open"] is False
    assert s[0]["since_previous_report"]["events"] == 0 and s[0]["last_event"]
    (second / "overview.md").write_text(
        "- **Agent session:** [Fix login](orca://session/s1) · x · status: done: merged\n"
    )
    close(second)
    third = runmod.open_run("daily")
    sessions.main(third)
    assert json.loads((third / "sessions.json").read_text()) == []


def test_a_missing_hook_file_is_not_checked(root, monkeypatch, tmp_path):
    monkeypatch.setattr(sessions, "HOOK_FILE", tmp_path / "none.json")
    f = runmod.open_run("daily")
    sessions.main(f)
    assert json.loads((f / "sessions-status.json").read_text())["read"] is False


# One item across GitHub, ClickUp and sessions (FR-28)


def sess(sid, branch, urls=(), events=3, **kw):
    base = {
        "session_id": sid,
        "title": f"session {sid}",
        "repo": "IronbellyOrg/Coder",
        "branch": branch,
        "worktree": "/w",
        "terminal_open": True,
        "claude_running": True,
        "linked_issue": None,
        "linked_pr": None,
        "events_total": events,
        "last_event": RECENT,
        "transcript": "/none",
        "read_offset": 0,
        "since_previous_report": dict(
            sessions.EMPTY,
            events=events,
            last_event=RECENT if events else None,
            prompt_urls=list(urls),
            item_urls=list(urls),
        ),
    }
    base.update(kw)
    return base


def cu(tid, **kw):
    base = {
        "source": "clickup",
        "org": "ClickUp",
        "repo": "Ops",
        "kind": "task",
        "number": tid,
        "title": f"Task {tid}",
        "url": f"https://app.clickup.com/t/{tid}",
        "author": "ryan",
        "assignees": [ME],
        "labels": [],
        "created": RECENT,
        "updated": RECENT,
        "comments": 0,
        "draft": None,
        "review_requests": [],
        "closes": [],
        "involves_person": False,
        "boards": [{"board": "ClickUp status", "status": "to do", "priority": None}],
        "location": "Ironbelly / Ops",
        "hierarchy": [],
        "waiting_on": [],
        "blocking": [],
        "github_links": [],
        "mentions_you": False,
    }
    base.update(kw)
    return base


JOIN_GITHUB = [
    item(1, assignees=[ME]),
    item(3, kind="pr", branch="fix-thing", clickup_refs=["86bbb"]),
]
JOIN_TASKS = [
    cu("86aaa", github_links=[f"{U}issues/1"]),
    cu("86bbb", assignees=[], author=ME),
    cu("86eee"),
]
JOIN_SESSIONS = [
    sess("s1", "fix-thing"),
    sess("s2", "1-start"),
    sess("s3", "main", urls=[f"{U}issues/1", f"{U}pull/3"]),
    sess("s4", "main", urls=["https://app.clickup.com/t/86eee"]),
]


def test_match_lists_each_thing_once_under_its_item(root):
    f = new_run(root, JOIN_GITHUB, tasks=JOIN_TASKS, sess=JOIN_SESSIONS)
    items = {i["url"]: i for i in json.loads((f / "items.json").read_text())}
    assert sorted(items) == [
        "https://app.clickup.com/t/86eee",
        f"{U}issues/1",
        f"{U}pull/3",
        "orca://session/s3",
    ]
    assert [t["number"] for t in items[f"{U}issues/1"]["clickup"]] == [
        "86aaa"
    ]  # the task links the issue
    assert [t["number"] for t in items[f"{U}pull/3"]["clickup"]] == [
        "86bbb"
    ]  # the pull request names the task
    assert [s["session_id"] for s in items[f"{U}pull/3"]["sessions"]] == [
        "s1"
    ]  # a pull request on its branch
    assert [s["session_id"] for s in items[f"{U}issues/1"]["sessions"]] == [
        "s2"
    ]  # its branch names #1
    assert [
        s["session_id"] for s in items["https://app.clickup.com/t/86eee"]["sessions"]
    ] == ["s4"]  # named once
    merged = json.loads((f / "merged-into.json").read_text())
    assert (
        merged["https://app.clickup.com/t/86aaa"] == f"{U}issues/1"
        and "orca://session/s3" not in merged
    )
    cls = json.loads((f / "classified.json").read_text())["items"]
    assert cls["orca://session/s3"]["group"] == "inprogress"
    assert cls[f"{U}pull/3"]["group"] == "owned"  # its session makes it Clay's work


def test_sessions_render_with_a_status_the_model_must_give(root):
    f = stub(root, JOIN_GITHUB, tasks=JOIN_TASKS, sess=JOIN_SESSIONS)
    text = (f / "overview.md").read_text()
    other = common.section(text, "Other work in progress")
    assert "](orca://session/s3)" in other and "{{RF_PLACEHOLDER:status:s3}}" in other
    assert "  - [Task 86aaa](https://app.clickup.com/t/86aaa)" in common.section(
        text, "Your work by priority"
    )
    fill(f, status="sleeping: no idea")
    code, out = check_exit(f)
    assert code == 1 and "sessions | FAIL" in out
    (f / "overview.md").write_text(
        (f / "overview.md")
        .read_text()
        .replace("sleeping: no idea", "progressed: wrote the fix")
    )
    code, out = check_exit(f)
    assert code == 0, out


def test_unchanged_sessions_carry_their_status_by_rule(root):
    first = stub(root, JOIN_GITHUB, tasks=JOIN_TASKS, sess=JOIN_SESSIONS)
    fill(first)
    text = re.sub(
        r"(\(orca://session/s1\)[^\n]*status: )progressed: it wrote the fix",
        r"\1waiting on you: asks which fix",
        (first / "overview.md").read_text(),
    )
    (first / "overview.md").write_text(text)
    close(first)
    second = stub(root, JOIN_GITHUB, tasks=JOIN_TASKS, sess=JOIN_SESSIONS)
    st = common.session_statuses((second / "overview.md").read_text())
    assert st["s1"] == "waiting on you: asks which fix" and st["s3"].startswith(
        "stalled: no activity after"
    )


def test_a_task_that_joins_an_item_leaves_through_closed_with_where_it_went(root):
    first = stub(root, JOIN_GITHUB, tasks=JOIN_TASKS + [cu("86fff")])
    finish(first)
    moved = JOIN_TASKS + [cu("86fff", github_links=[f"{U}pull/3"])]
    second = stub(root, JOIN_GITHUB, tasks=moved)
    closed = common.section(
        (second / "overview.md").read_text(), "Closed since the previous report"
    )
    assert (
        f"Task 86fff](https://app.clickup.com/t/86fff): now listed under Item 3 ({U}pull/3)"
        in closed
    )


# Review findings 2026-10-30 (qa/qa-awr-sessions-match-review.md)


def comment(cid, date, text, tag=None, **kw):
    parts = [{"type": "tag", "user": {"id": tag}}] if tag else []
    return dict(
        {
            "id": cid,
            "date": date,
            "comment_text": text,
            "comment": parts,
            "user": {"username": "ryan"},
        },
        **kw,
    )


def test_clickup_finds_watched_and_mentioned_tasks_and_pages_comments(
    root, monkeypatch
):
    raw = {
        "tasks": RAW["tasks"]
        + [
            task("86eee", "Watched", watchers=[{"id": 42}]),
            task("86fff", "Watched, quiet", watchers=[{"id": 42}]),
        ]
    }
    page1 = [comment(str(i), RECENT_MS, f"note {i}") for i in range(25)]
    page2 = [comment("m", RECENT_MS, "@Clay please look", tag=42)]
    fake_api(
        monkeypatch,
        pages=(raw,),
        updated={"86aaa", "86ddd", "86eee"},
        comments={"86ddd": [page1, page2]},
    )
    f = runmod.open_run("daily")
    clickup.main(f)
    got = {t["number"]: t for t in json.loads((f / "clickup-items.json").read_text())}
    assert "86eee" in got and "86fff" not in got  # watched: listed only when it changed
    assert got["86ddd"][
        "mentions_you"
    ]  # someone else's task, but a comment on its second page tags Clay
    events = json.loads((f / "clickup-events.json").read_text())["comments"]
    assert len(events["https://app.clickup.com/t/86ddd"]) == 26


def test_a_quiet_watched_task_leaves_with_a_true_reason(root, monkeypatch):
    raw = {"tasks": RAW["tasks"] + [task("86eee", "Watched", watchers=[{"id": 42}])]}
    fake_api(monkeypatch, pages=(raw,))
    first = runmod.open_run("daily")
    clickup.main(first)
    (first / "github-items.json").write_text("[]")
    (first / "coverage.json").write_text(json.dumps(COVERAGE_OK))
    for step in (match, classify, compare):
        step.main(first)
    close(first)
    fake_api(monkeypatch, pages=(raw,), updated=set())
    second = runmod.open_run("daily")
    clickup.main(second)
    gone = json.loads((second / "clickup-gone.json").read_text())
    assert gone["https://app.clickup.com/t/86eee"].startswith(
        "still open, but you only watch it"
    )


def test_a_rate_limit_is_waited_out(monkeypatch):
    import urllib.error

    class Ok(io.BytesIO):
        headers = {}

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    answers = [
        urllib.error.HTTPError("u", 429, "slow down", {"X-RateLimit-Reset": "0"}, None),
        Ok(b'{"user": {"id": 1}}'),
    ]
    monkeypatch.setenv("CLICKUP_API_TOKEN", "not-a-real-token")
    monkeypatch.setattr(
        clickup.urllib.request,
        "urlopen",
        lambda req, timeout: (
            (_ for _ in ()).throw(answers.pop(0))
            if isinstance(answers[0], Exception)
            else answers.pop(0)
        ),
    )
    monkeypatch.setattr(clickup.time, "sleep", lambda s: None)
    assert clickup.call("GET", "/v2/user") == {"user": {"id": 1}}


def test_a_failed_dm_reply_read_is_not_checked(root, monkeypatch):
    fake_api(monkeypatch)
    clickup.send_dm("hello")
    fake_api(monkeypatch, dm_fails=True)
    f = runmod.open_run("daily")
    clickup.main(f)
    assert json.loads((f / "clickup-replies.json").read_text()) == []
    (f / "github-items.json").write_text("[]")
    (f / "coverage.json").write_text(json.dumps(COVERAGE_OK))
    for step in (match, classify, compare, render):
        step.main(f)
    assert "your ClickUp DM replies: not read (GET" in common.section(
        (f / "overview.md").read_text(), "Not checked"
    )


def test_clickups_own_branch_names_match():
    assert collect.clickup_refs("", "", "CU-86abc12_Fix-login_Clay-Phi") == ["86abc12"]
    assert match.BRANCH_CU.findall("CU-86abc12_Fix-login_Clay-Phi") == ["86abc12"]


def test_a_forks_pull_request_on_main_matches_no_session(root):
    fork = item(9, kind="pr", branch="main", cross_repo=True)
    f = new_run(root, [fork], sess=[sess("s1", "main")])
    assert "orca://session/s1" in {
        i["url"] for i in json.loads((f / "items.json").read_text())
    }


def test_a_prompt_match_lasts_after_the_prompt_window(root):
    s = sess(
        "s1", "main", prompt_urls_all=[f"{U}issues/1"]
    )  # asked in an earlier report, nothing new now
    f = new_run(root, JOIN_GITHUB, sess=[s])
    assert (
        json.loads((f / "merged-into.json").read_text())["orca://session/s1"]
        == f"{U}issues/1"
    )


def test_unread_sessions_keep_their_items_and_groups(root):
    lone = [
        item(5, title="Someone else's issue"),
        item(3, kind="pr", branch="fix-thing"),
    ]
    first = stub(root, lone, sess=[sess("s1", "fix-thing")])
    finish(first)
    second = stub(root, lone)  # no sessions-status.json: sessions were not read
    items = {i["url"]: i for i in json.loads((second / "items.json").read_text())}
    assert items[f"{U}pull/3"]["sessions"][0]["carried"] is True
    assert (
        json.loads((second / "classified.json").read_text())["items"][f"{U}pull/3"][
            "group"
        ]
        == "owned"
    )
    text = (second / "overview.md").read_text()
    assert (
        "no longer yours" not in text
        and "(kept as it was: sessions not read this run)" in text
    )


def test_a_session_item_is_carried_while_sessions_are_not_read(root):
    first = stub(root, [], sess=[sess("s9", "main")])
    fill(first)
    close(first)
    second = new_run(root, [])  # no sessions-status.json: sessions not read
    compare.main(second)
    assert (
        "orca://session/s9"
        in json.loads((second / "compare.json").read_text())["carried"]
    )


def test_sessions_survive_a_run_that_could_not_read_them(
    root, orca_sessions, monkeypatch, tmp_path
):
    state, path = orca_sessions
    first = runmod.open_run("daily")
    sessions.main(first)
    (first / "overview.md").write_text(
        "- **Agent session:** [Fix login](orca://session/s1) · x · status: progressed: wrote it\n"
    )
    close(first)
    hook = sessions.HOOK_FILE
    monkeypatch.setattr(sessions, "HOOK_FILE", tmp_path / "gone.json")
    second = runmod.open_run("daily")
    sessions.main(second)
    close(second)
    monkeypatch.setattr(sessions, "HOOK_FILE", hook)
    state["terminals"] = []
    third = runmod.open_run("daily")
    sessions.main(third)
    got = json.loads((third / "sessions.json").read_text())
    assert [s["session_id"] for s in got] == ["s1"] and got[0]["title"] == "Fix login"
    x = got[0][
        "since_previous_report"
    ]  # nothing new: it still ends on the unanswered Bash call
    assert (
        x["events"] == 0
        and x["pending_tool_call"]["tool"] == "Bash"
        and x["state_from_earlier"]
    )


def test_a_line_still_being_written_is_read_next_time(tmp_path):
    p = tmp_path / "t.jsonl"
    first = line("user", RECENT, "first prompt") + "\n"
    second = line("user", RECENT, "second prompt") + "\n"
    p.write_text(first + second[:30])
    facts, end = sessions.extract(p, 0, first_report=False)
    assert [x["text"] for x in facts["prompts"]] == ["first prompt"] and end == len(
        first
    )
    p.write_text(first + second)
    facts, end = sessions.extract(p, end, first_report=False)
    assert [x["text"] for x in facts["prompts"]] == ["second prompt"] and end == len(
        first + second
    )


# Review pass 2 findings (qa/qa-awr-sessions-match-review-pass-2.md)


def test_a_done_session_closes_after_an_unread_run(root):
    first = stub(root, [], sess=[sess("s9", "main")])
    fill(first, status="done: finished and merged")
    close(first)
    second = stub(root, [])  # sessions not read: s9 is carried
    fill(second)
    close(second)
    third = new_run(
        root, [], sess=[]
    )  # read again; sessions.py dropped s9 because a report called it done
    compare.main(third)
    c = json.loads((third / "compare.json").read_text())
    assert (
        c["closed"]["orca://session/s9"]["reason"]
        == "its agent session's work was reported done"
    )


def test_a_cu_branch_session_keeps_its_item_when_clickup_is_not_read(root):
    gh = [item(5)]
    tasks = [cu("86abc", assignees=[], github_links=[f"{U}issues/5"])]
    s = [sess("s1", "CU-86abc_Fix-login_Clay")]
    first = stub(root, gh, tasks=tasks, sess=s)
    assert (
        json.loads((first / "merged-into.json").read_text())["orca://session/s1"]
        == f"{U}issues/5"
    )
    finish(first)
    second = new_run(root, gh, sess=s)  # ClickUp not read
    items = {i["url"]: i for i in json.loads((second / "items.json").read_text())}
    assert [x["session_id"] for x in items[f"{U}issues/5"]["sessions"]] == [
        "s1"
    ] and "orca://session/s1" not in items


def test_a_carried_session_keeps_its_last_status_instead_of_asking(root):
    lone = [item(3, kind="pr", branch="fix-thing")]
    first = stub(root, lone, sess=[sess("s1", "fix-thing")])
    fill(first, status="waiting on you: asks which fix")
    close(first)
    second = stub(
        root, [dict(lone[0], comments=4)]
    )  # changed on GitHub, sessions not read
    text = (second / "overview.md").read_text()
    assert "{{RF_PLACEHOLDER:status:s1}}" not in text
    assert (
        "status: waiting on you: asks which fix (kept as it was: sessions not read this run)"
        in text
    )


def test_a_post_is_never_sent_twice(monkeypatch):
    sent = []

    def urlopen(req, timeout):
        sent.append(req.get_method())
        raise TimeoutError("the reply stalled after ClickUp took the message")

    monkeypatch.setenv("CLICKUP_API_TOKEN", "not-a-real-token")
    monkeypatch.setattr(clickup.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(clickup.time, "sleep", lambda s: None)
    with pytest.raises(clickup.ClickUpError):
        clickup.call(
            "POST", "/v3/workspaces/900/chat/channels/dm1/messages", {"content": "x"}
        )
    assert sent == ["POST"]


def test_a_session_is_never_named_after_its_orca_terminal(
    root, orca_sessions, tmp_path
):
    state, path = orca_sessions
    hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    path.write_text(
        line("user", hour_ago, "tidy the docs") + "\n"
    )  # no Claude title yet
    state["terminals"][0]["title"] = "Claude Code"
    f = runmod.open_run("daily")
    sessions.main(f)
    assert json.loads((f / "sessions.json").read_text())[0]["title"] == "tidy the docs"


def test_a_session_on_a_clickup_only_task_keeps_it_when_clickup_is_not_read(root):
    tasks = [cu("86abc")]
    s = [sess("s1", "CU-86abc_Fix-login_Clay")]
    first = stub(root, [], tasks=tasks, sess=s)
    finish(first)
    second = stub(root, [], sess=s)  # ClickUp not read
    items = {i["url"]: i for i in json.loads((second / "items.json").read_text())}
    task_ = items["https://app.clickup.com/t/86abc"]
    assert (
        task_["carried"]
        and [x["session_id"] for x in task_["sessions"]] == ["s1"]
        and "orca://session/s1" not in items
    )
    c = json.loads((second / "compare.json").read_text())
    url = "https://app.clickup.com/t/86abc"
    assert (
        not c["closed"]
        and url not in c["new"]
        and url in c["carried"]
        and url not in c["unchanged"]
    )
    text = (second / "overview.md").read_text()
    assert "| Carried, source not read | 1 |" in text
    assert "carried: its source was not read this run" in common.entry_blocks(text)[url]


def test_change_notes_and_times_read_as_plain_english():
    cmp_ = {
        "new": [],
        "carried": [],
        "previous_run": "x",
        "changed": {
            f"{U}issues/1": {
                "board_status": {"was": ["Dev: Backlog"], "now": ["Dev: Ready"]},
                "comments": {"was": 0, "now": 1},
                "assignees": {"was": [], "now": [ME]},
            }
        },
    }
    note = render.change_note(f"{U}issues/1", cmp_)
    assert (
        note
        == "changed: assignees none to clayphi; board status Dev: Backlog to Dev: Ready; 1 new comments"
    )
    assert common.local_time("2026-11-03T13:00:00+00:00") == "2026-11-03 07:00 CST"
    assert common.local_time("2026-10-30T12:00:00Z") == "2026-10-30 07:00 CDT"


def test_render_replaces_dashes_copied_from_titles(root):
    f = stub(
        root, ITEMS + [item(30, assignees=[ME], title="CanExport \N{EN DASH} Claims")]
    )
    assert (
        "\N{EN DASH}" not in (f / "overview.md").read_text()
        and "CanExport - Claims" in (f / "overview.md").read_text()
    )


def test_needs_you_is_exactly_the_sessions_waiting_on_you(root):
    # 2026-11-05: "Needs you" is agent sessions stopped and waiting on Clay, checked both ways.
    f = waiting_run(root)
    fill(f, status="waiting on you: asks which fix")
    code, out = check_exit(f)
    assert (
        code == 1
        and "session orca://session/s3 is waiting on you but has no Needs you entry"
        in out
    )
    base = (f / "overview.md").read_text()
    good = base.replace("Nothing new needs you.", ask(3, "Pick the fix"))
    (f / "overview.md").write_text(good)
    assert "needs-you | PASS" in check_exit(f)[1]
    assert f"- {common.NOT_ASKED}" in common.section(
        good, "Not checked"
    )  # said every run
    cases = [  # each departure from the rule or from templates/needs-you-template.md fails
        (
            "\n## Your work by priority",
            f"\n{need('Coder issue #1', f'{U}issues/1', 'Review the plan')}\n## Your work by priority",
            "is not an agent session waiting on you",
        ),
        (
            "status: waiting on you: asks which fix",
            "status: progressed: it wrote the fix",
            "is not an agent session waiting on you",
        ),
        (
            f"It works on [Coder pull request #3]({U}pull/3).",
            "It works on the login fix.",
            "does not link the item its session works on",
        ),
        (
            "- **What it is:** It works",
            "- **What it is:** it works",
            "'What it is' has a line that does not start with a capital",
        ),
        (
            "- **Recommendation:** Merge it, because its checks pass.\n",
            "",
            "its bullets are not the template's",
        ),
        (
            "- **Where it stands:** It waits on you.\n",
            "It waits on you, as a paragraph.\n",
            "has text outside its bullets",
        ),
        (
            "### [Session s3](orca://session/s3): Pick",
            "### Pick",
            "does not start with its linked agent session",
        ),
    ]
    for old, new, why in cases:
        (f / "overview.md").write_text(good.replace(old, new, 1))
        out = check_exit(f)[1]
        assert "needs-you | FAIL" in out and why in out, (why, out)


# No failed report reaches Clay (Clay, 2026-11-03)


def test_the_gate_blocks_a_report_until_the_checks_pass_on_its_exact_text(root):
    f = stub(root)
    fill(f)
    assert "the script checks have not all passed" in runmod.passed(f)[1]
    approve(f)
    assert runmod.passed(f) == (True, "")
    # An edit after the checks (Clay's priority change during the run): the hash no longer matches.
    (f / "overview.md").write_text(
        (f / "overview.md").read_text() + "\nmade High after the check\n"
    )
    assert "changed after the last script check" in runmod.passed(f)[1]
    with pytest.raises(SystemExit) as e:
        runmod.close_run(f)
    assert "not closed" in str(e.value.code) and not (f / "complete.json").exists()


def test_the_gate_needs_every_script_check_including_links(root):
    f = stub(root)
    fill(f)
    approve(f)
    checks = f / "script-checks.md"
    checks.write_text(checks.read_text().replace("| links | PASS | ok |\n", ""))
    assert "links; run check.py --links" in runmod.passed(f)[1]


def test_a_report_that_has_not_passed_is_never_sent(root, monkeypatch):
    calls = fake_api(monkeypatch)
    f = stub(root)
    fill(
        f,
        needs=f"### [Coder pull request #3]({U}pull/3): Approve the merge\nAbout [Item 3]({U}pull/3).",
    )
    runmod.write_summary(f)
    with pytest.raises(SystemExit):
        clickup.dm(f, f / "summary.md")
    assert not any(m == "POST" for m, _ in calls)
    assert json.loads((f / "clickup-dm.json").read_text())["detail"].startswith(
        "blocked:"
    )
    approve(f)
    good = (f / "summary.md").read_text()
    for bad in (
        good.replace("(1)", "(3)"),
        good.replace("**Your work:** ", "**Your work:** 999 assigned; "),
        good + "extra words by hand\n",
    ):
        (f / "summary.md").write_text(
            bad
        )  # anything but the script's own summary is refused, by the gate too
        assert "not the one run.py summary makes" in runmod.deliverable(f)[1]
        with pytest.raises(SystemExit):
            clickup.dm(f, f / "summary.md")
        assert not any(m == "POST" for m, _ in calls)
    (f / "summary.md").write_text(good)
    (f / "other.md").write_text(good)
    with pytest.raises(SystemExit) as e:
        clickup.dm(f, f / "other.md")
    assert "only the run's own summary.md" in str(e.value.code)
    with pytest.raises(SystemExit) as e:
        clickup.dm(f, f / "summary.md")
    assert e.value.code == 0 and any(m == "POST" for m, _ in calls)


def test_the_summary_is_built_from_the_report_by_script(root):
    first = stub(root)
    finish(first)
    f = stub(root)
    fill(f, needs=need("Coder pull request #3", f"{U}pull/3", "Approve the merge"))
    runmod.write_summary(f)
    s = (f / "summary.md").read_text()
    assert "## Needs you (1)" in s and "| Assigned to you |" not in s
    assert (
        f"**[Coder pull request #3]({U}pull/3): Approve the merge**\n- **What it is:** A fix for the login page.\n"
        "- **Where it stands:** It waits on you.\n- **Question:** Merge it?\n"
        "- **Why this reaches you:** Row 8 of the escalation table: a merge waits on your answer.\n"
        "- **Low-stakes options:** None.\n"
        "- **Recommendation:** Merge it, because its checks pass.\n"
        "- **If you do not answer:** The merge stays blocked until you answer.\n"
    ) in s
    assert "It ships today" not in s  # the options stay on the page
    assert "Assigned to you 2" in s and "{{" not in s and common.REPORT_URL in s
    assert (
        re.search(r"Since the previous report \(\w{3} \d{4}-\d{2}-\d{2}\)", s)
        and "yesterday" not in s
    )


def test_a_daily_run_without_a_report_is_abandoned_never_closed(root, monkeypatch):
    f = runmod.open_run("daily")
    with pytest.raises(SystemExit) as e:
        runmod.close_run(f)
    assert "overview.md is missing" in str(e.value.code)
    runmod.abandon_run(f, "collect.py crashed")
    assert (f / "abandoned.json").exists() and not (f / "complete.json").exists()
    assert (
        not (root / ".dev" / "coordinator" / "run.lock").exists()
        and runmod.latest_completed() is None
    )
    monkeypatch.setattr(waker, "local_gate", lambda mode, now=None: None)
    waker.check_missed()
    assert last_wake(root)["outcome"].startswith(
        "DM_NEEDED: no daily report has finished"
    )


def test_a_session_that_stopped_on_its_reply_may_be_waiting_on_you(root):
    # 2026-11-03: the last reply ended "Say the word and I'll run it." with no question mark.
    s = [sess("s1", "fix-thing")]
    s[0]["since_previous_report"]["replies"] = [
        {"time": RECENT, "text": "Say the word and I'll run it."}
    ]
    lone = [item(3, kind="pr", branch="fix-thing")]
    f = stub(root, lone, sess=s)
    fill(f, status="waiting on you: asks to run the bump")
    text = (
        (f / "overview.md")
        .read_text()
        .replace(
            "Nothing new needs you.",
            f"### Run the bump\nThe session on [Item 3]({U}pull/3) asks.",
        )
    )
    (f / "overview.md").write_text(text)
    assert "sessions | PASS" in check_exit(f)[1]


# Code review findings 2026-11-03 (qa/qa-awr-waker-and-rules-review.md)


def test_start_session_never_types_where_someone_is_typing(root, monkeypatch):
    o = FakeOrca(
        [term(handle="term_shell")], live=[], prompt={"term_shell"}, draft="my-ot"
    )
    o.install(monkeypatch)
    handle = waker.start_session(common.workspace_path(), [o.terms[0]])
    assert handle == "term_new" and o.created == ["term_new"] and "my-ot" == o.draft


def test_the_name_question_is_found_above_blank_rows(root, monkeypatch):
    o = FakeOrca([term(handle="term_shell")], live=[], prompt={"term_shell"})
    o.install(monkeypatch)
    monkeypatch.setattr(
        waker.orca_term,
        "screen",
        lambda h: {
            "draft": "",
            "tail": (
                ["Session name (Enter = untagged, Ctrl+C = plain shell): ", "", "", ""]
                if h in o.prompt
                else []
            ),
        },
    )
    assert waker.start_session(common.workspace_path(), [o.terms[0]]) == "term_shell"
    assert o.sent == ["coordinator"] and not o.created


def test_a_session_that_never_starts_says_so(root, monkeypatch):
    o = FakeOrca([], live=[])
    o.install(monkeypatch)
    monkeypatch.setattr(
        waker.orca_term,
        "send",
        lambda h, text, **kw: o.sent.append(text) or {"stages": []},
    )
    monkeypatch.setattr(waker, "START_WAIT_S", 0)
    waker.wake("morning")
    assert last_wake(root)["outcome"].startswith(
        "DM_NEEDED: the coordinator session did not start"
    )


def test_a_new_session_that_is_not_ready_is_retried_not_dmed(root, monkeypatch):
    o = FakeOrca([], live=[], idle=False)
    o.install(monkeypatch)
    waker.wake("morning")
    rec = last_wake(root)
    assert (
        rec["attempts"] == 2 and o.sent[0] == "coordinator"
    )  # retried; the second attempt found it live but busy


def test_two_live_sessions_reach_needs_you(root):
    f = runmod.open_run("daily")
    (f / "wake-records.json").write_text(
        json.dumps([{"mode": "morning", "other_live_sessions": ["term_old"]}])
    )
    for name, data in (("github-items.json", ITEMS), ("coverage.json", COVERAGE_OK)):
        (f / name).write_text(json.dumps(data))
    for step in (match, classify, compare, render):
        step.main(f)
    text = (
        f / "overview.md"
    ).read_text()  # a notice about the helper leads the report; it is not a "Needs you"
    assert (
        "**Two coordinator sessions are running:**" in text.split("\n## ", 1)[0]
        and "`term_old`" in text
    )
    assert "Two coordinator" not in common.section(text, "Needs you")
    assert "**Two coordinator sessions are running:**" in runmod.build_summary(f)


def test_no_hourly_check_on_weekends(root, monkeypatch):
    monkeypatch.setattr(waker, "COORDINATOR_BUILT", True)
    assert "no report on Sunday" in waker.local_gate(
        "hourly", datetime(2026, 11, 8, 15, 0, tzinfo=timezone.utc)
    )


def test_the_summary_reads_only_the_count_table_and_keeps_missed_days(root):
    first = stub(root)
    finish(first)
    f = stub(root)
    fill(
        f,
        needs=f"### Pick a format\nAbout [Item 3]({U}pull/3).\n\n| Formats asked about | 4 |\n|---|---|\n",
    )
    text = (f / "overview.md").read_text()
    text = text.replace(
        "\n\n| Your work | Count |",
        "\n**Missed reports:** no report on Fri 2026-10-30.\n\n| Your work | Count |",
        1,
    )
    (f / "overview.md").write_text(text)
    s = runmod.build_summary(f)
    assert "Formats asked about" not in s and "judged in the report 1" in s
    assert s.index("**Missed reports:** no report on Fri 2026-10-30.") < s.index(
        "**Your work:**"
    )


# The report page (CLAY, 2026-11-04: merge in the open-work.html format; the Markdown report is illegible)


def page_data(folder):
    text = (folder / "report.html").read_text()
    return json.loads(
        re.search(
            r'<script id="data" type="application/json">(.*?)</script>', text, re.S
        ).group(1)
    )


def test_the_page_shows_each_item_with_its_notes_and_they_carry_to_the_next_day(root):
    first = stub(root)
    finish(first)  # builds the page and notes.json
    d = page_data(first)
    one = next(i for i in d["items"] if i["url"] == f"{U}issues/1")
    assert (
        one["state"] == "In progress"
        and one["what"] == "A fix for the login page."
        and one["next"] == "Ryan reviews it."
    )
    assert (root / ".dev" / "coordinator" / "report.html").read_text() == (
        first / "report.html"
    ).read_text()
    second = stub(
        root
    )  # nothing changed: no item needs writing, every card keeps its notes
    assert json.loads((second / "to-write.json").read_text()) == []
    assert "RF_PLACEHOLDER:state" not in (second / "overview.md").read_text()
    fill(second)
    approve(second)
    one = next(i for i in page_data(second)["items"] if i["url"] == f"{U}issues/1")
    assert one["sections"] == [
        lbl for lbl, _ in common.ITEM_SECTIONS
    ]  # the template, in order
    shown = one[
        "parts"
    ]  # every part shown as a bullet, a bulleted part nested under its label (CLAY, 2026-11-05)
    assert shown.startswith(
        '<ul class="parts"><li><strong>What it is:</strong> A fix for the login page.</li>'
    )
    assert (
        f"<li><strong>Current state:</strong> {NOW}</li>" in shown
        and one["asOf"]
        and one["change"] == "No change"
    )
    assert (
        "<li><strong>Done, with evidence:</strong><ul><li>The fix is written and its checks pass.</li></ul></li>"
        in shown
    )
    assert [lbl for lbl in re.findall(r"<li><strong>([^<]+):</strong>", shown)] == one[
        "sections"
    ]
    assert one["owner"] == "You (assigned to you)"
    runmod.close_run(second)
    third = stub(root, [dict(i, comments=2) if i["number"] == 1 else i for i in ITEMS])
    assert json.loads((third / "to-write.json").read_text()) == [
        f"{U}issues/1"
    ]  # only the changed one


def test_the_gate_refuses_a_missing_or_stale_page(root):
    f = stub(root)
    fill(f)
    approve(f)
    runmod.write_summary(f)
    assert runmod.deliverable(f) == (True, "")
    (f / "report.html").unlink()
    assert "report.html is missing" in runmod.deliverable(f)[1]
    page.main(f)
    (f / "overview.md").write_text((f / "overview.md").read_text() + "\nedited\n")
    approve_checks_only = (
        (f / "script-checks.md").read_text().split("overview sha256:")[0]
    )
    (f / "script-checks.md").write_text(
        approve_checks_only + f"overview sha256: {runmod.sha256(f / 'overview.md')}\n"
    )
    assert "built from an older overview.md" in runmod.deliverable(f)[1]


def test_item_text_cannot_add_html_to_the_page(root):
    f = stub(
        root, ITEMS + [item(20, assignees=[ME], title='<img src=x onerror="alert(1)">')]
    )
    fill(
        f,
        needs=need(
            "Coder pull request #3",
            f"{U}pull/3",
            "Pick <b>one</b>",
            what="Say <script>no</script> to [it](https://github.com/IronbellyOrg/Coder/pull/3).",
        ),
    )
    approve(f)
    html_ = (f / "report.html").read_text()
    data = page_data(f)
    assert "<script>no" not in html_ and "&lt;script&gt;no" in data["needs"][0]["body"]
    assert "&lt;b&gt;one" in data["needs"][0]["title"]
    assert (
        '<a href="https://github.com/IronbellyOrg/Coder/pull/3"'
        in data["needs"][0]["body"]
    )
    assert next(i for i in data["items"] if i["url"] == f"{U}issues/20")[
        "title"
    ].startswith("<img")  # escaped by the page script
    assert "esc(it.title)" in (common.SKILL_DIR / "templates" / "report.js").read_text()


def test_links_open_in_the_same_tab(root):
    # 2026-11-05: Orca's browser blocks links that open a new window, so they did nothing when Clay clicked them.
    f = stub(root)
    fill(f, needs=need("Coder pull request #3", f"{U}pull/3", "Approve the merge"))
    approve(f)
    page_html = (f / "report.html").read_text()
    assert (
        f'<a href=\\"{U}pull/3\\">' in page_html or f'<a href="{U}pull/3">' in page_html
    )
    assert "_blank" not in page_html


def test_needs_you_and_items_follow_the_priority_protocol(root):
    # 2026-11-05: the first "Needs you" was not the most important one; everything sorts by level, then state.
    f = waiting_run(root, (3, 4))
    fill(
        f,
        needs=ask(4, "Low one") + "\n" + ask(3, "Urgent one"),
        status="waiting on you: asks which fix",
    )
    text = (f / "overview.md").read_text()
    blocks = common.entry_blocks(text)
    for u, level in (
        (f"{U}pull/3", "Urgent"),
        (f"{U}pull/4", "Low"),
    ):  # the model's suggested levels
        text = text.replace(
            blocks[u],
            blocks[u].replace("· Suggested Medium ·", f"· Suggested {level} ·", 1),
        )
    (f / "overview.md").write_text(text)
    assert check_exit(f)[0] == 0
    approve(f)
    assert [n["title"].split("</a>: ")[1] for n in page_data(f)["needs"]] == [
        "Urgent one",
        "Low one",
    ]
    s = runmod.build_summary(f)
    assert s.index("Urgent one") < s.index("Low one")
    one = next(i for i in page_data(f)["items"] if i["url"] == f"{U}pull/3")
    assert (
        one["priority"] == "Urgent" and one["suggested"] and one["rank"] == [0, 4]
    )  # Urgent, In progress


def test_clickup_tasks_with_no_github_link_are_kept_apart(root):
    tasks = [cu("86aaa", github_links=[f"{U}issues/1"]), cu("86zzz")]
    f = stub(root, [item(1, assignees=[ME])], tasks=tasks)
    fill(f)
    approve(f)
    by_url = {i["url"]: i for i in page_data(f)["items"]}
    assert (
        by_url["https://app.clickup.com/t/86zzz"]["clickupOnly"] is True
    )  # its own section at the bottom
    assert not by_url[f"{U}issues/1"]["clickupOnly"]


# PR C: the skill runs from the orchestrator repo, and the orchestrator's living report (spec DQ12, 6.4)
#
# The entry file below is built from the slot list of spec 5.3 wave 3: every slot of common.WRITTEN, plus
# `suggested` and `priority_why` when the priority is Unset, plus `session_status`; the fixed fields are the
# ones documented in common.py. PR B's `report-entry` writes the same shape.

HELD = f"{U}issues/1"
HELD_PR = f"{U}pull/10"
HELD_TWO = f"{U}issues/11"
NOW_ISO = datetime.now(timezone.utc).isoformat(timespec="seconds")
HELD_ITEMS = ITEMS + [
    item(10, kind="pr", author=ME, closes=[HELD], branch="1-start"),
    item(11, assignees=[ME]),
]
HELD_SESSIONS = [sess("w1", "1-start"), sess("o1", "main"), sess("w2", "11-start")]


def held_entry(number=1, **kw):
    """The entry file of one issue the orchestrator holds, as `report-entry` writes it."""
    one = number == 1
    e = {
        "url": f"{U}issues/{number}",
        "title": f"Item {number}",
        "kind": "orchestrated",
        "group": "assigned",
        "priority": "High",
        "assignees": [ME],
        "human_assignee": ME,
        "orchestrator": {
            "id": "coder-1",
            "tag": "orchestrator-coder-1",
            "session_id": "o1",
            "link": "orca://session/o1",
            "tier": "tier1b",
        },
        "worker": {
            "session_ids": ["w1" if one else "w2"],
            "link": f"orca://session/{'w1' if one else 'w2'}",
            "title": f"Worker for issue {number}",
            "branch": f"{number}-start",
            "tier": "tier2",
        },
        "pr_url": HELD_PR if one else None,
        "last_update": NOW_ISO,
        "follow_up_state": "working" if one else "delivered",
        "state": "In progress" if one else "Ready to merge",
        "next": "The worker finishes the fix.",
        "what": "A fix for the login page.",
        "state_text": "The worker has opened its pull request.",
        "done": "- The worker opened its pull request.",
        "todo": "- The reviewers finish.",
        "happened": "- The worker opened pull request 10 today.\n- Its checks pass.",
        "recommend": "Let the orchestrator merge it once the reviews finish.",
        "needs": "N/A",
        "how": "The orchestrator's own records.",
        "session_status": (
            {"w1": "working: it writes the fix", "o1": "working: it watches the worker"}
            if one
            else {
                "w2": "done: it reports the work finished",
                "o1": "working: it watches",
            }
        ),
    }
    e.update(kw)
    return e


def put_entry(root, key, entry, sub=""):
    d = root / ".dev" / "coordinator" / "orchestrated"
    d = d / sub if sub else d
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{key}.json").write_text(json.dumps(entry))
    return d / f"{key}.json"


def put_both(root):
    put_entry(root, "IronbellyOrg__Coder__1", held_entry(1))
    put_entry(root, "IronbellyOrg__Coder__11", held_entry(11))


def written_urls(folder):
    """Every url the run's files carry for an item (the files the spec 9.1 row names)."""
    out = {}
    for name in ("github-items", "items", "classified", "compare", "to-write"):
        out[name] = (folder / f"{name}.json").read_text()
    return out


def fake_gh(monkeypatch, answers):
    """`gh issue view <n> --repo <r> --json ...` answers by issue number; nothing else is allowed to run."""
    calls = []

    def gh(*args):
        calls.append(args)
        assert args[:2] == ("issue", "view"), args
        what = answers[int(args[2])]
        if isinstance(what, Exception):
            raise what
        return what

    monkeypatch.setattr(runmod, "gh_json", gh)

    def no_command(*a, **kw):
        raise AssertionError(f"refresh ran a command: {a}")

    monkeypatch.setattr(runmod, "run_cmd", no_command)
    return calls


OPEN_MINE = {"state": "OPEN", "stateReason": None, "assignees": [{"login": ME}]}


def closed_daily_run(root, items=HELD_ITEMS, **kw):
    f = stub(root, items, sess=HELD_SESSIONS, **kw)
    fill(f)
    assert check_exit(f)[0] == 0
    runmod.write_summary(f)
    approve(f)
    assert runmod.deliverable(f) == (True, "")
    runmod.close_run(f)
    return f


# repo_root and the config


def test_repo_root_is_awr_root_else_the_orchestrator_repo_of_the_poll_config(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("AWR_ROOT", str(tmp_path / "set"))
    assert common.repo_root() == tmp_path / "set"
    assert common.workspace_path() == str(tmp_path / "set")
    monkeypatch.delenv("AWR_ROOT")
    home, repo = tmp_path / "home", tmp_path / "orchestrator"
    monkeypatch.setenv("HOME", str(home))
    with pytest.raises(SystemExit) as e:  # no poll configuration at all
        common.repo_root()
    assert "AWR_ROOT" in str(e.value)
    cfg = home / ".config" / "superclaude" / "issue-watch.json"
    cfg.parent.mkdir(parents=True)
    cfg.write_text(json.dumps({"orchestrator_repo": str(repo)}))
    repo.mkdir()
    with pytest.raises(SystemExit) as e:  # the repo has no repos.yaml
        common.repo_root()
    assert "repos.yaml" in str(e.value)
    (repo / "repos.yaml").write_text("schema_version: 1\n")
    assert common.repo_root() == repo
    cfg.write_text(json.dumps({"orchestrator_repo": "relative/path"}))
    with pytest.raises(SystemExit):  # a relative path is no path
        common.repo_root()


def test_the_config_has_no_workspace_key_and_no_script_reads_one():
    assert "workspace" not in common.CONFIG
    for script in SCRIPTS.glob("*.py"):
        assert 'CONFIG["workspace"]' not in script.read_text(), script.name


# exclude.py


def test_a_daily_run_leaves_out_an_issue_the_orchestrator_holds(root):
    closed_daily_run(root)  # the run before the orchestrator claimed issue 1
    put_both(root)
    changed = [
        dict(i, comments=2) if i["number"] in (1, 5, 10, 11) else i for i in HELD_ITEMS
    ]
    second = stub(root, changed, sess=HELD_SESSIONS)
    # The held issues, the pull request and the worker and orchestrator sessions are in no run file...
    for name, text in written_urls(second).items():
        for url in (HELD, HELD_TWO, HELD_PR):
            assert url not in text, (name, url)
    assert "orca://session/w1" not in (second / "items.json").read_text()
    excluded = json.loads((second / "excluded.json").read_text())
    assert excluded == sorted(
        [HELD, HELD_TWO, HELD_PR] + [f"orca://session/{s}" for s in ("o1", "w1", "w2")]
    )
    text = (second / "overview.md").read_text()
    for gone in (
        "IronbellyOrg-Coder-issue-1}",
        "IronbellyOrg-Coder-pr-10",
        "session-w1",
    ):
        assert gone not in text
    assert f"]({HELD})" not in text and "orca://session/w1" not in text
    # ...while the same change on an item with no entry file is listed as changed, queued and marked.
    five = f"{U}issues/5"
    assert five in json.loads((second / "compare.json").read_text())["changed"]
    assert five in json.loads((second / "to-write.json").read_text())
    assert common.UPDATE_MARK in common.entry_blocks(text)[five]
    assert text.count(common.UPDATE_MARK) == 1
    # check.py passes and the gate does not block.
    fill(second)
    assert check_exit(second)[0] == 0
    runmod.write_summary(second)
    approve(second)
    assert runmod.deliverable(second) == (True, "")


def test_without_excluded_json_the_carry_forward_check_reports_the_held_item_lost(root):
    closed_daily_run(root)
    put_both(root)
    second = stub(root, HELD_ITEMS, sess=HELD_SESSIONS)
    fill(second)
    assert check_exit(second)[0] == 0
    (second / "excluded.json").write_text("[]")
    code, text = check_exit(second)
    assert code == 1 and HELD in text and "carry-forward | FAIL" in text


@pytest.mark.parametrize(
    "case",
    [
        "closed by a person",
        "unassigned",
        "repo not read",
        "closed folder",
        "info folder",
    ],
)
def test_an_entry_the_run_does_not_show_open_and_assigned_excludes_nothing(root, case):
    items = HELD_ITEMS
    coverage = COVERAGE_OK
    sub = ""
    if case == "closed by a person":
        items = [i for i in HELD_ITEMS if i["number"] != 1]
    elif case == "unassigned":
        items = [dict(i, assignees=[]) if i["number"] == 1 else i for i in HELD_ITEMS]
    elif case == "repo not read":
        coverage = dict(
            COVERAGE_OK,
            repos=[dict(COVERAGE_OK["repos"][0], errors=["issues: HTTP 502"])],
        )
    else:
        sub = "closed" if case == "closed folder" else "info"
    put_entry(root, "IronbellyOrg__Coder__1", held_entry(1), sub=sub)
    f = stub(root, items, coverage=coverage, sess=HELD_SESSIONS)
    assert json.loads((f / "excluded.json").read_text()) == []
    urls = {i["url"] for i in json.loads((f / "github-items.json").read_text())}
    assert HELD_PR in urls  # the pull request stays
    assert (HELD in urls) == (case != "closed by a person")
    assert (
        "orca://session/w1"
        in (f / "items.json").read_text() + (f / "sessions.json").read_text()
    )


def test_exclude_gives_the_same_result_run_twice(root):
    put_both(root)
    f = new_run(root, HELD_ITEMS, sess=HELD_SESSIONS)
    first = {
        n: (f / n).read_text()
        for n in ("github-items.json", "sessions.json", "excluded.json")
    }
    exclude.main(f)
    assert first == {n: (f / n).read_text() for n in first}


def test_a_clickup_task_linked_to_a_held_issue_is_an_item_of_its_own(root):
    put_entry(root, "IronbellyOrg__Coder__1", held_entry(1))
    f = stub(root, [item(1, assignees=[ME])], tasks=[cu("86aaa", github_links=[HELD])])
    items = {i["url"]: i for i in json.loads((f / "items.json").read_text())}
    assert list(items) == ["https://app.clickup.com/t/86aaa"]
    assert "https://app.clickup.com/t/86aaa" in (f / "overview.md").read_text()
    fill(f)
    assert check_exit(f)[0] == 0


# render.py and the daily report's own shape


def header_line(block):
    return next(ln for ln in block.splitlines() if ln.startswith("**Opened by:**"))


def test_a_daily_item_keeps_the_ironflow_header_line(root):
    f = stub(root)
    block = common.entry_blocks((f / "overview.md").read_text())[HELD]
    assert header_line(block) == (
        "**Opened by:** someone · **Assigned to:** clayphi · "
        "**Owner:** You (assigned to you) · **Board:** Not on a board"
    )
    assert "Orchestrator" not in block


def test_a_needs_you_entry_led_by_a_session_the_orchestrator_holds_is_not_carried(root):
    prev = "## Needs you\n\n" + need("worker", "orca://session/w1", "Pick the fix")
    kept, _ = render.still_waiting(prev, "", set(), held=set())
    assert len(kept) == 1
    assert render.still_waiting(prev, "", set(), held={"orca://session/w1"}) == ([], [])


# The report templates: the three escalation lines


def test_the_two_templates_carry_the_three_escalation_lines():
    for name in ("needs-you-template.md", "item-template.md"):
        text = (SCRIPTS.parent / "templates" / name).read_text()
        for line in common.ESCALATION_LINES:
            assert line in text.replace("**", ""), (name, line)


@pytest.mark.parametrize(
    "label", ["Why this reaches you", "Low-stakes options", "If you do not answer"]
)
def test_check_fails_a_needs_you_entry_without_an_escalation_line(root, label):
    session = "orca://session/s3"
    good = need("Session s3", session, "Pick the fix")
    assert check.needs_problems(good.strip("\n")) == []
    bad = re.sub(rf"- \*\*{label}:\*\*[^\n]*\n", "", good)
    assert "its bullets are not the template's" in "; ".join(
        check.needs_problems(bad.strip("\n"))
    )


def test_an_escalation_in_an_entry_file_needs_the_three_lines_in_its_own_part(root):
    esc = (
        "Decide whether to publish the release.\n"
        "Why this reaches you: row 1, a release is tagged.\n"
        "Low-stakes options: none.\n"
        "If you do not answer: the release stays unpublished."
    )
    e = held_entry(1, needs=esc)
    item_, cls_, _ = runmod.entry_record(HELD, e, "k", False, "")
    cmp_ = {"new": [], "changed": {}, "carried": [], "closed": {}, "unchanged": []}
    ctx = {
        "template": render.item_template(),
        "notes": {},
        "to_write": set(),
        "statuses": {},
        "prev_date": "",
    }
    block = render.entry(HELD, item_, cls_, cmp_, ctx, filed=e)
    assert check.template_problems(HELD, block, orchestrated=True) == []
    assert (
        "\n### " not in "\n" + block
    )  # no heading of its own: it is lines of the issue's entry
    cut = e["needs"].replace("Low-stakes options: none.\n", "")
    block = render.entry(HELD, item_, cls_, cmp_, ctx, filed=held_entry(1, needs=cut))
    assert "lacks 'Low-stakes options:'" in "; ".join(
        check.template_problems(HELD, block, orchestrated=True)
    )
    # Not an escalation: no line is required, and the daily report's own items are never asked for them.
    quiet = render.entry(HELD, item_, cls_, cmp_, ctx, filed=held_entry(1))
    assert check.template_problems(HELD, quiet, orchestrated=True) == []


# run.py refresh


def test_refresh_builds_the_shared_page_after_a_daily_run_closes(root, monkeypatch):
    put_both(root)
    daily = closed_daily_run(root)
    own_page = (daily / "report.html").read_text()
    shared = root / ".dev" / "coordinator" / "report.html"
    assert (
        HELD not in shared.read_text()
    )  # the daily page has no block for a held issue
    calls = fake_gh(monkeypatch, {1: OPEN_MINE, 11: OPEN_MINE})
    runmod.refresh()
    assert [c[2] for c in calls] == [
        "1",
        "11",
    ]  # only `gh issue view`, once per entry file
    data = json.loads(
        re.search(
            r'<script id="data" type="application/json">(.*?)</script>',
            shared.read_text(),
            re.S,
        ).group(1)
    )
    urls = {i["url"] for i in data["items"]}
    assert {HELD, HELD_TWO} <= urls  # a block for each entry file...
    cls = json.loads((daily / "classified.json").read_text())
    listed = {u for u in cls["order"] if cls["items"][u]["group"] in render.LISTED}
    assert listed <= urls  # ...and for each item the daily run wrote
    assert (
        daily / "report.html"
    ).read_text() == own_page  # <run>/report.html is not touched
    assert runmod.deliverable(daily) == (True, "")  # so the gate still passes
    assert not (root / ".dev" / "coordinator" / runmod.REFRESH_SCRATCH).exists()


def test_a_refreshed_entry_shows_its_own_text_and_its_session_statuses(
    root, monkeypatch
):
    put_both(root)
    closed_daily_run(root)
    fake_gh(monkeypatch, {1: OPEN_MINE, 11: OPEN_MINE})
    runmod.refresh()
    shared = root / ".dev" / "coordinator" / "report.html"
    data = json.loads(
        re.search(
            r'<script id="data" type="application/json">(.*?)</script>',
            shared.read_text(),
            re.S,
        ).group(1)
    )
    cards = {i["url"]: i for i in data["items"]}
    one, two = cards[HELD], cards[HELD_TWO]
    assert (
        "The worker opened pull request 10 today." in one["parts"]
        and "Its checks pass." in one["parts"]
    )
    assert "Nothing since" not in one["parts"] and "Nothing since" not in two["parts"]
    assert [s["state"] for s in one["sessions"]] == [
        "working",
        "working",
    ]  # not "stalled"
    assert [s["state"] for s in two["sessions"] if s["url"].endswith("w2")] == ["done"]
    assert one["state"] == "In progress" and two["state"] == "Ready to merge"
    assert "orca://session/o1" in one["parts"] and "orca://session/w1" in one["parts"]
    assert data["needs"] == []  # no "Needs you" entry is made for an orchestrated issue


def test_a_refreshed_block_names_the_orchestrator_and_never_prints_nothing_since(root):
    e = held_entry(1)
    item_, cls_, _ = runmod.entry_record(HELD, e, "k", False, "")
    cmp_ = {"new": [], "changed": {}, "carried": [], "closed": {}, "unchanged": [HELD]}
    ctx = {
        "template": render.item_template(),
        "notes": {},
        "to_write": set(),
        "statuses": {},
        "prev_date": "2026-11-18",
    }
    block = render.entry(HELD, item_, cls_, cmp_, ctx, filed=e)
    assert header_line(block).endswith(
        "**Orchestrator:** [orchestrator-coder-1](orca://session/o1) (tier1b)"
    )
    assert "Nothing since" not in block and common.UPDATE_MARK not in block
    assert "RF_PLACEHOLDER" not in block and "{{" not in block
    assert (
        "status: working: it writes the fix" in block
    )  # the entry's status, not carried_status
    assert check.template_problems(HELD, block) == []


def test_refresh_moves_a_closed_or_unassigned_issue_and_keeps_an_open_one(
    root, monkeypatch
):
    for n in (1, 11, 12, 13):
        put_entry(
            root, f"IronbellyOrg__Coder__{n}", held_entry(n, url=f"{U}issues/{n}")
        )
    fake_gh(
        monkeypatch,
        {
            1: {
                "state": "CLOSED",
                "stateReason": "COMPLETED",
                "assignees": [{"login": ME}],
            },
            11: {"state": "CLOSED", "stateReason": "NOT_PLANNED", "assignees": []},
            12: {
                "state": "OPEN",
                "stateReason": None,
                "assignees": [{"login": "ryan"}],
            },
            13: OPEN_MINE,
        },
    )
    runmod.refresh()
    folder = root / ".dev" / "coordinator" / "orchestrated"
    assert sorted(p.name for p in folder.glob("*.json")) == [
        "IronbellyOrg__Coder__13.json"
    ]
    reasons = {
        p.stem: json.loads(p.read_text())["close_reason"]
        for p in (folder / "closed").glob("*.json")
    }
    assert reasons == {
        "IronbellyOrg__Coder__1": "COMPLETED",
        "IronbellyOrg__Coder__11": "NOT_PLANNED",
        "IronbellyOrg__Coder__12": "no longer assigned to you",
    }
    assert "closed_at" in json.loads(
        (folder / "closed" / "IronbellyOrg__Coder__1.json").read_text()
    )


def test_a_failed_github_read_closes_no_entry(root, monkeypatch, capsys):
    put_entry(root, "IronbellyOrg__Coder__1", held_entry(1))
    fake_gh(monkeypatch, {1: common.CommandError("HTTP 502")})
    runmod.refresh()
    assert (
        root / ".dev" / "coordinator" / "orchestrated" / "IronbellyOrg__Coder__1.json"
    ).exists()
    assert "HTTP 502" in capsys.readouterr().err


def test_refresh_deletes_closed_and_info_files_older_than_info_ttl_days(
    root, monkeypatch
):
    old = (datetime.now(timezone.utc) - timedelta(days=15)).isoformat()
    new = (datetime.now(timezone.utc) - timedelta(days=13)).isoformat()
    put_entry(
        root,
        "IronbellyOrg__Coder__2",
        held_entry(1, closed_at=old, close_reason="COMPLETED"),
        sub="closed",
    )
    put_entry(
        root,
        "IronbellyOrg__Coder__3",
        held_entry(1, closed_at=new, close_reason="COMPLETED"),
        sub="closed",
    )
    put_entry(
        root,
        "mention__IronbellyOrg__Coder__4",
        held_entry(1, kind="info:mentions", last_update=old),
        sub="info",
    )
    put_entry(
        root,
        "mention__IronbellyOrg__Coder__5",
        held_entry(1, kind="info:mentions", last_update=new),
        sub="info",
    )
    fake_gh(monkeypatch, {})
    runmod.refresh()
    base = root / ".dev" / "coordinator" / "orchestrated"
    assert sorted(p.name for p in (base / "closed").glob("*.json")) == [
        "IronbellyOrg__Coder__3.json"
    ]
    assert sorted(p.name for p in (base / "info").glob("*.json")) == [
        "mention__IronbellyOrg__Coder__5.json"
    ]
    # One key sets both ages: a repos.yaml with info_ttl_days: 3 keeps nothing 13 days old.
    (root / "repos.yaml").write_text("schema_version: 1\ninfo_ttl_days: 3\n")
    runmod.refresh()
    assert (
        list((base / "closed").glob("*.json")) == []
        and list((base / "info").glob("*.json")) == []
    )


def test_refresh_without_run_does_nothing_while_a_daily_run_holds_the_lock(
    root, monkeypatch, capsys
):
    put_entry(root, "IronbellyOrg__Coder__1", held_entry(1))
    calls = fake_gh(monkeypatch, {1: OPEN_MINE})
    f = stub(root, sess=HELD_SESSIONS)  # opens a run: the lock is held
    assert runmod.refresh() is None
    assert calls == [] and not (root / ".dev" / "coordinator" / "report.html").exists()
    assert "holds the run lock" in capsys.readouterr().out
    other = f.parent / "20200101T000000Z-daily"
    other.mkdir()
    assert runmod.refresh(other) is None  # --run of a run that does not hold the lock
    fill(f)
    runmod.refresh(f)  # --run of the run that holds it: allowed
    assert (root / ".dev" / "coordinator" / "report.html").exists()
    assert not (f / "report.html").exists()  # never <run>/report.html


def test_refresh_with_no_daily_report_yet_shows_the_entries_alone(root, monkeypatch):
    put_both(root)
    fake_gh(monkeypatch, {1: OPEN_MINE, 11: OPEN_MINE})
    runmod.refresh()
    shared = root / ".dev" / "coordinator" / "report.html"
    data = json.loads(
        re.search(
            r'<script id="data" type="application/json">(.*?)</script>',
            shared.read_text(),
            re.S,
        ).group(1)
    )
    assert {i["url"] for i in data["items"]} == {HELD, HELD_TWO}


def test_an_information_entry_already_in_the_daily_report_is_left_out(
    root, monkeypatch
):
    daily = closed_daily_run(root, [item(5, author=ME), item(7, involves_person=True)])
    seven = f"{U}issues/7"
    assert f"]({seven})" in (daily / "overview.md").read_text()
    put_entry(
        root,
        "mention__IronbellyOrg__Coder__7",
        held_entry(1, url=seven, kind="info:mentions"),
        sub="info",
    )
    put_entry(
        root,
        "mention__IronbellyOrg__Coder__9",
        held_entry(1, url=f"{U}issues/9", kind="info:mentions"),
        sub="info",
    )
    fake_gh(monkeypatch, {})
    runmod.refresh()
    shared = (root / ".dev" / "coordinator" / "report.html").read_text()
    data = json.loads(
        re.search(
            r'<script id="data" type="application/json">(.*?)</script>', shared, re.S
        ).group(1)
    )
    urls = [i["url"] for i in data["items"]]
    assert f"{U}issues/9" in urls and seven not in urls


def test_a_refreshed_page_lists_what_the_orchestrator_closed_and_drops_held_blocks(
    root, monkeypatch
):
    daily = closed_daily_run(
        root
    )  # issue 1 is a block of this daily report: it is held since
    assert HELD in (daily / "overview.md").read_text()
    put_entry(root, "IronbellyOrg__Coder__1", held_entry(1))
    put_entry(
        root,
        "IronbellyOrg__Coder__21",
        held_entry(
            1,
            url=f"{U}issues/21",
            title="Gone",
            close_reason="COMPLETED",
            closed_at=NOW_ISO,
        ),
        sub="closed",
    )
    fake_gh(monkeypatch, {1: OPEN_MINE})
    runmod.refresh()
    shared = (root / ".dev" / "coordinator" / "report.html").read_text()
    data = json.loads(
        re.search(
            r'<script id="data" type="application/json">(.*?)</script>', shared, re.S
        ).group(1)
    )
    assert [i["url"] for i in data["items"]].count(
        HELD
    ) == 1  # the old daily block is not shown twice
    assert any("COMPLETED" in line and "Gone" in line for line in data["closed"])
