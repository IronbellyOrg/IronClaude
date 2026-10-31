"""Codex review threads handled like Augment (design .dev/pr-submit-codex/design/, sections
7-12, 16 and the section 18 amendments).

Fixtures ``codex-clean-pr334.json`` and ``codex-findings-pr336.json`` are slimmed live
poll snapshots of PRs 334 and 336 (IronbellyOrg/IronClaude, 2026-10-31): Codex-authored
bodies are verbatim, other bodies are cut, the head is set to the commit the Codex
marker reviewed, and in the PR 336 fixture the three Codex threads are re-opened.
"""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
from pathlib import Path

import pytest

from superclaude.pr_submit import (
    DetectionContract,
    EventType,
    Finding,
    MonitorState,
    actionable_finding_comments,
    augment_wait_outcome,
    classify,
    classify_codex,
    codex_finding_comments,
    codex_review_state,
    codex_severity_hint,
    codex_wait_outcome,
    dedup_groups,
    finding_from_comment,
    has_augment_activity,
    merge_wait,
    parse_codex_priority,
    pending_retriggers,
    remap_severity,
    retrigger_phrase,
    reviewer_activity,
    route,
)
from superclaude.pr_submit.recovery import (
    BRANCH_A_LANDED,
    detect_crash_window,
    resolve_crash_window,
)
from superclaude.pr_submit.run_log import RunLog

CONTRACT = DetectionContract.load()
CODEX = "chatgpt-codex-connector"


def badge(alt: str, url: str, title: str = "Fix it") -> str:
    return (
        f"**<sub><sub>![{alt} Badge](https://img.shields.io/badge/{url}-yellow"
        f"?style=flat)</sub></sub>  {title}**\n\nBody text.\n\n"
        "<!-- codex-code-review-finding:v1 -->"
    )


@pytest.fixture
def clean334(load_fixture):
    return load_fixture("codex-clean-pr334.json")


@pytest.fixture
def findings336(load_fixture):
    return load_fixture("codex-findings-pr336.json")


def summary(snapshot: dict) -> dict:
    return next(c for c in snapshot["comments"] if "codex-review-state:v1" in c["body"])


def codex_review(snapshot: dict) -> dict:
    return next(r for r in snapshot["reviews"] if r["user"]["login"].startswith(CODEX))


# --- 1. badge parsing ------------------------------------------------------------


@pytest.mark.parametrize("priority", ["P0", "P1", "P2", "P3"])
def test_badge_priorities_parse(priority):
    assert parse_codex_priority(badge(priority, priority)) == priority


@pytest.mark.parametrize(
    "body",
    [
        "**Fix it**\n\nno badge here",
        badge("P1", "P1") + "\n" + badge("P2", "P2"),
        badge("P4", "P4"),
        badge("P1", "P2"),
        "An intro line first\n" + badge("P2", "P2"),
        None,
    ],
    ids=["none", "two-badges", "P4", "alt-url-mismatch", "not-first-line", "no-body"],
)
def test_malformed_badges_give_no_priority(body):
    assert parse_codex_priority(body) is None


def test_real_pr336_bodies_are_p2(findings336):
    bodies = [
        t["comments"]["nodes"][0]["body"]
        for t in findings336["threads"]
        if t["comments"]["nodes"][0]["author"]["login"] == CODEX
    ]
    assert [parse_codex_priority(b) for b in bodies] == ["P2", "P2", "P2"]


# --- 2. severity mapping -----------------------------------------------------------


@pytest.mark.parametrize(
    ("body", "expected_route"),
    [
        (badge("P0", "P0"), "--depth deep --fix"),
        (badge("P1", "P1"), "--depth deep --fix"),
        (badge("P2", "P2"), "--fix"),
        (badge("P3", "P3"), "report-only"),
        (badge("P1", "P2"), "--fix"),  # malformed -> Medium fail-safe
    ],
)
def test_priority_routes_like_augment_severity(body, expected_route):
    hint = codex_severity_hint(parse_codex_priority(body))
    raw = {"path": "a.py", "line": 1, "body": body, "reviewer": "codex"}
    finding = remap_severity(finding_from_comment({**raw, "severity_hint": hint}))
    assert finding.reviewer == "codex"
    assert route(finding) == expected_route


# --- 3. Codex completion and gate states ------------------------------------------


def test_pr334_shape_is_clean(clean334):
    assert classify_codex(clean334, CONTRACT) == "clean"
    assert codex_finding_comments(clean334, CONTRACT) == []


def test_pr336_shape_has_three_p2_findings(findings336):
    assert classify_codex(findings336, CONTRACT) == "findings"
    roots = codex_finding_comments(findings336, CONTRACT)
    assert len(roots) == 3
    assert {
        (r["reviewer"], r["codex_priority"], r["severity_hint"]) for r in roots
    } == {("codex", "P2", "medium")}
    findings = [remap_severity(finding_from_comment(r)) for r in roots]
    assert {route(f) for f in findings} == {"--fix"}
    assert {f.comment_id for f in findings} == {4432330726, 4432330727, 4432330729}


def test_resolved_codex_threads_with_review_on_head_are_clean(findings336):
    for thread in findings336["threads"]:
        thread["isResolved"] = True
    assert classify_codex(findings336, CONTRACT) == "clean"


def test_findings_promised_but_not_visible_keep_polling(clean334):
    marker = summary(clean334)
    marker["body"] = marker["body"].replace(
        '"has_any_findings":false', '"has_any_findings":true', 1
    )
    assert classify_codex(clean334, CONTRACT) == "polling"


def _replace_in_summary(old: str, new: str):
    def mutate(snapshot: dict) -> None:
        comment = summary(snapshot)
        comment["body"] = comment["body"].replace(old, new, 1)

    return mutate


@pytest.mark.parametrize(
    "mutate",
    [
        _replace_in_summary('"completed"', '"running"'),
        lambda s: s.update(head_sha="0" * 40),
        _replace_in_summary('{"code_review"', '{"code_review" x'),
        _replace_in_summary('{"code_review":', '{"code_review":{},"code_review":'),
        lambda s: s.update(observed_at="2026-10-31T15:59:00Z"),
        lambda s: s.update(threads_ok=False),
        lambda s: summary(s).pop("updated_at"),
    ],
    ids=[
        "running",
        "wrong-head",
        "malformed-json",
        "duplicate-key",
        "after-observed",
        "incomplete-snapshot",
        "no-update-time",
    ],
)
def test_invalid_or_incomplete_codex_evidence_polls(findings336, mutate):
    mutate(findings336)
    assert classify_codex(findings336, CONTRACT) == "polling"
    assert codex_finding_comments(findings336, CONTRACT) == []


def test_completion_must_be_newer_than_watermark(findings336):
    late = "2026-10-31T23:00:00Z"
    early = "2026-10-31T15:00:00Z"
    assert classify_codex(findings336, CONTRACT, watermark=late) == "polling"
    assert classify_codex(findings336, CONTRACT, watermark=early) == "findings"


def test_a1_completion_is_later_of_marker_and_head_review(findings336):
    """A1: roots created after the marker edit are still selected through the review."""
    summary(findings336)["updated_at"] = "2026-10-31T15:57:20Z"  # before the roots
    codex_review(findings336)["submitted_at"] = "2026-10-31T15:57:40Z"
    state = codex_review_state(findings336, CONTRACT)
    assert state["completed_at"].isoformat() == "2026-10-31T15:57:40+00:00"
    assert classify_codex(findings336, CONTRACT) == "findings"
    # Without the review time the roots (15:57:29) are newer than completion: polling.
    codex_review(findings336)["commit_id"] = "1" * 40
    assert classify_codex(findings336, CONTRACT) == "polling"


def test_a3_newest_codex_marker_wins(findings336):
    second = copy.deepcopy(summary(findings336))
    findings336["comments"].append(second)
    assert classify_codex(findings336, CONTRACT) == "polling"  # same time: ambiguous
    second["updated_at"] = "2026-10-31T16:30:00Z"
    findings336["observed_at"] = "2026-10-31T23:00:00Z"
    assert classify_codex(findings336, CONTRACT) == "findings"
    second["body"] = second["body"].replace('"completed"', '"running"', 1)
    assert classify_codex(findings336, CONTRACT) == "polling"  # newest is running


def test_a6_codex_root_after_marker_and_review_submission_is_counted(findings336):
    """A6 (PR 337): roots of the head review count even when posted after it."""
    summary(findings336)["updated_at"] = "2026-10-31T15:57:20Z"
    codex_review(findings336)["submitted_at"] = "2026-10-31T15:57:25Z"  # roots :29
    assert classify_codex(findings336, CONTRACT) == "findings"
    assert len(codex_finding_comments(findings336, CONTRACT)) == 3
    # A review that is not on the head does not vouch for its roots.
    codex_review(findings336)["commit_id"] = "1" * 40
    assert classify_codex(findings336, CONTRACT) == "polling"


def test_a3_older_malformed_marker_does_not_block_a_newer_valid_one(findings336):
    """PR 337 review: a malformed older marker is superseded by a newer valid one."""
    older = copy.deepcopy(summary(findings336))
    older["id"] += 1
    older["updated_at"] = "2026-10-31T15:00:00Z"
    older["body"] = older["body"].replace('{"code_review"', '{"code_review" x', 1)
    findings336["comments"].insert(0, older)
    assert classify_codex(findings336, CONTRACT) == "findings"
    # A malformed marker that is the newest still polls (never falls back).
    older["updated_at"] = "2026-10-31T16:30:00Z"
    findings336["observed_at"] = "2026-10-31T23:00:00Z"
    assert classify_codex(findings336, CONTRACT) == "polling"


# --- 4. reviewer detection and the merge -------------------------------------------


def _only(payload, keep_codex):
    """Keep only Codex activity (keep_codex) or only non-Codex activity."""
    out = copy.deepcopy(payload)

    def is_codex(login):
        return login.startswith(CODEX)

    out["reviews"] = [
        r for r in out["reviews"] if is_codex(r["user"]["login"]) == keep_codex
    ]
    out["comments"] = [
        c for c in out["comments"] if is_codex(c["user"]["login"]) == keep_codex
    ]
    out["threads"] = [
        t
        for t in out["threads"]
        if is_codex(t["comments"]["nodes"][0]["author"]["login"]) == keep_codex
    ]
    return out


def test_reviewer_activity_augment_only_codex_only_both_neither(findings336):
    assert reviewer_activity(findings336, CONTRACT) == {"augment": True, "codex": True}
    assert reviewer_activity(_only(findings336, keep_codex=False), CONTRACT) == {
        "augment": True,
        "codex": False,
    }
    assert reviewer_activity(_only(findings336, keep_codex=True), CONTRACT) == {
        "augment": False,
        "codex": True,
    }
    empty = {"reviews": [], "comments": [], "threads": []}
    assert reviewer_activity(empty, CONTRACT) == {"augment": False, "codex": False}


def test_augment_activity_predicate_is_unchanged_for_thread_roots():
    """reviewer_activity['augment'] stays has_augment_activity (reviews/comments)."""
    root = {"author": {"login": "augmentcode"}, "body": "x"}
    payload = {
        "reviews": [],
        "comments": [],
        "threads": [{"comments": {"nodes": [root]}}],
    }
    assert reviewer_activity(payload, CONTRACT)["augment"] is False
    assert has_augment_activity(payload, CONTRACT) is False


KW = {"elapsed": 60, "timeout": 600, "silence_timeout": 300}
AT_DEADLINE = {"elapsed": 300, "timeout": 600, "silence_timeout": 300}
AT_TIMEOUT = {"elapsed": 600, "timeout": 600, "silence_timeout": 300}


def test_augment_only_pr_codex_absent_once_augment_settles():
    aug = augment_wait_outcome("findings", MonitorState.S2_CLASSIFY)
    cdx = codex_wait_outcome("polling", active=False, other_settled=True, **KW)
    assert cdx == "absent"
    result = merge_wait((aug, "findings"), (cdx, "polling"))
    assert result == {
        "outcome": "findings",
        "used": ["augment"],
        "absent": ["codex"],
        "incomplete": [],
    }


def test_codex_only_pr_continues_when_augment_is_silent():
    """A2: Augment's silence outcome with Codex present does not end the run."""
    aug = augment_wait_outcome("polling", MonitorState.TERMINAL_AUGMENT_NO_RESPONSE)
    cdx = codex_wait_outcome("findings", active=True, other_settled=True, **KW)
    result = merge_wait((aug, "polling"), (cdx, "findings"))
    assert (result["outcome"], result["used"], result["absent"]) == (
        "findings",
        ["codex"],
        ["augment"],
    )


def test_a2_absent_reviewer_is_never_pending():
    """A2: an already-absent Augment does not hold a finished Codex in S5."""
    silent = augment_wait_outcome("polling", MonitorState.S2_CLASSIFY)
    assert silent == "pending"
    aug = augment_wait_outcome("polling", MonitorState.S2_CLASSIFY, absent=True)
    cdx = codex_wait_outcome("clean", active=True, other_settled=False, **KW)
    assert merge_wait((silent, "polling"), (cdx, "clean"))["outcome"] == "polling"
    assert merge_wait((aug, "polling"), (cdx, "clean"))["outcome"] == "clean"
    assert (
        codex_wait_outcome(
            "polling", active=True, other_settled=False, absent=True, **KW
        )
        == "absent"
    )


def test_both_reviewers_present_merge_findings():
    result = merge_wait(("done", "clean"), ("done", "findings"))
    assert result["outcome"] == "findings"
    assert result["used"] == ["augment", "codex"]


def test_neither_reviewer_present_is_no_response():
    aug = augment_wait_outcome("polling", MonitorState.TERMINAL_AUGMENT_NO_RESPONSE)
    cdx = codex_wait_outcome("polling", active=False, other_settled=True, **AT_DEADLINE)
    assert merge_wait((aug, "polling"), (cdx, "polling"))["outcome"] == "no_response"


@pytest.mark.parametrize(
    ("augment", "codex", "outcome"),
    [
        (("pending", "polling"), ("done", "clean"), "polling"),
        (("done", "clean"), ("pending", "polling"), "polling"),
        (("done", "declined"), ("done", "findings"), "declined"),
        (("done", "clean"), ("incomplete", "polling"), "clean"),
        (("incomplete", "polling"), ("done", "clean"), "clean"),
        (("incomplete", "polling"), ("absent", "polling"), "timeout"),
        (("incomplete", "polling"), ("incomplete", "polling"), "timeout"),
        (("absent", "polling"), ("incomplete", "polling"), "timeout"),
    ],
)
def test_merge_table_rows(augment, codex, outcome):
    assert merge_wait(augment, codex)["outcome"] == outcome


def test_codex_inactive_waits_only_until_silence_deadline():
    def outcome(active, **times):
        return codex_wait_outcome(
            "polling", active=active, other_settled=False, **times
        )

    assert outcome(False, **KW) == "pending"
    assert outcome(False, **AT_DEADLINE) == "absent"
    assert outcome(True, **AT_TIMEOUT) == "incomplete"


# --- 5. Augment classification is unchanged by Codex threads -----------------------


def test_codex_roots_never_leak_into_augment_selection(load_fixture):
    snap = load_fixture("cosmos-pr266.json")
    snap["threads"][0]["isResolved"] = False
    augment = DetectionContract(
        augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode"
    )
    watermark = "2026-10-16T19:30:00Z"
    before = actionable_finding_comments(snap, augment, watermark=watermark)
    codex_thread = copy.deepcopy(snap["threads"][0])
    codex_thread["id"] = "PRRT_codex_example"
    root = codex_thread["comments"]["nodes"][0]
    root.update(id="PRRC_codex", databaseId=9999999, author={"login": CODEX})
    snap["threads"].append(codex_thread)
    assert classify(snap, augment, watermark=watermark) == "findings"
    assert actionable_finding_comments(snap, augment, watermark=watermark) == before


# --- 7. dedup across reviewers ------------------------------------------------------


def test_dedup_groups_same_line_across_reviewers(findings336):
    roots = codex_finding_comments(findings336, CONTRACT)
    codex = [finding_from_comment(r) for r in roots]
    augment = Finding(
        path=codex[0].path,
        line=None,
        original_line=codex[0].original_line,
        body="staged changes are omitted",
        reviewer="augment",
    )
    elsewhere = Finding(path="other.md", line=7, body="x", reviewer="augment")
    groups = dedup_groups([augment, *codex, elsewhere])
    assert [len(g) for g in groups] == [2, 1, 1, 1]
    assert [f.reviewer for f in groups[0]] == ["augment", "codex"]
    assert sum(len(g) for g in groups) == 5
    assert dedup_groups([]) == []


# --- 8. run-log folds, re-trigger bookkeeping and resume ---------------------------


def test_event_enum_has_the_two_reviewer_events():
    assert len(EventType) == 41
    assert {EventType.REVIEWER_ABSENT.value, EventType.REVIEWER_INCOMPLETE.value} == {
        "reviewer_absent",
        "reviewer_incomplete",
    }


def test_two_reviewer_retrigger_counts_once_and_absent_rebuilds(tmp_path):
    rl = RunLog(336, tmp_path)
    for reviewer in ("augment", "codex"):
        rl.append(
            {
                "event_type": "rereview_requested",
                "cycle_id": "c1",
                "reviewer": reviewer,
            }
        )
    rl.append({"event_type": "reviewer_absent", "reviewer": "codex"})
    state = rl.rebuild_state()
    assert state["rereview_request_count"] == 1
    assert state["absent_reviewers"] == ["codex"]


def test_a4_crash_between_posts_reposts_only_the_missing_reviewer(tmp_path):
    """A4: the crash leaves only Augment's re-trigger; resume posts Codex only, on the
    dangling cycle_id, and reads each reviewer's watermark from its event timestamp."""
    rl = RunLog(337, tmp_path)
    rl.append(
        {
            "event_type": "push_initiated",
            "target_sha": "shaX",
            "idempotency_key": "push:r:c1:preX:feat",
            "run_id": "r",
            "cycle_id": "c1",
            "pre_push_sha": "preX",
            "target_branch": "feat",
            "target_remote": "origin",
        }
    )
    rl.append(
        {
            "event_type": "rereview_requested",
            "cycle_id": "c1",
            "reviewer": "augment",
            "timestamp": "2026-10-31T10:00:01Z",
        }
    )
    dangling = detect_crash_window(rl)
    branch, resume_state = resolve_crash_window(rl, dangling, remote_reachable=True)
    assert (branch, resume_state) == (
        BRANCH_A_LANDED,
        MonitorState.S5_AWAITING_REREVIEW,
    )
    events = rl.read_events()
    present = ["augment", "codex"]
    assert pending_retriggers(events, dangling["cycle_id"], present) == ["codex"]
    watermarks = {
        e.get("reviewer", "augment"): e["timestamp"]
        for e in events
        if e["event_type"] == "rereview_requested" and e["cycle_id"] == "c1"
    }
    assert watermarks == {"augment": "2026-10-31T10:00:01Z"}


def test_fixtures_are_complete_snapshots(load_fixture):
    for name in ("codex-clean-pr334.json", "codex-findings-pr336.json"):
        snap = load_fixture(name)
        assert snap["reviews_ok"] and snap["comments_ok"] and snap["threads_ok"]
        assert json.loads(json.dumps(snap)) == snap


# --- 9. shell adapters on a Codex thread (design sections 10 and 11) ---------------

SCRIPTS = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-pr-submit-protocol/scripts"
)
FAKE_GH = r"""#!/usr/bin/env bash
set -euo pipefail
jq -nc --args '$ARGS.positional' -- "$@" >> "$STUB_DIR/calls.jsonl"
field() {
    local name="$1" arg
    for arg in "${@:2}"; do
        if [[ "$arg" == "$name="* ]]; then printf '%s' "${arg#*=}"; return; fi
    done
}
[ "$1" = api ] || exit 92
if [[ " $* " == *" --method POST "* ]]; then
    target=""
    for arg in "$@"; do [[ "$arg" == repos/* ]] && target="$arg"; done
    case "$target" in
        */pulls/336/comments/*/replies)
            cid="${target%/replies}"; cid="${cid##*/}"
            jq -nc --argjson cid "$cid" '{id:999, in_reply_to_id:$cid}' ;;
        */issues/336/comments) printf '{"id":1}\n' ;;
        *) exit 93 ;;
    esac
    exit 0
fi
if [ "$2" = graphql ]; then
    query="$(field query "$@")"
    if [[ "$query" == *'mutation('* ]]; then
        jq -nc --arg tid "$(field threadId "$@")" \
            '{data:{resolveReviewThread:{thread:{id:$tid, isResolved:true}}}}'
        exit 0
    fi
    cat "$STUB_DIR/threads.json"
    exit 0
fi
exit 99
"""


@pytest.fixture
def fake_gh(tmp_path):
    gh = tmp_path / "gh"
    gh.write_text(FAKE_GH, encoding="utf-8")
    gh.chmod(0o755)

    def run(script, *args):
        result = subprocess.run(
            [str(SCRIPTS / script), *args],
            capture_output=True,
            text=True,
            timeout=30,
            env={
                **os.environ,
                "PATH": f"{tmp_path}:{os.environ['PATH']}",
                "STUB_DIR": str(tmp_path),
            },
        )
        calls_file = tmp_path / "calls.jsonl"
        calls = [
            json.loads(line)
            for line in (
                calls_file.read_text().splitlines() if calls_file.exists() else []
            )
        ]
        return result, calls

    return tmp_path, run


def _thread_page(threads):
    nodes = [
        {
            "id": t["id"],
            "isResolved": t["isResolved"],
            "comments": {
                "nodes": [
                    {
                        "databaseId": t["comments"]["nodes"][0]["databaseId"],
                        "replyTo": None,
                    }
                ]
            },
        }
        for t in threads
    ]
    page = {"hasNextPage": False, "endCursor": "c1"}
    return {
        "data": {
            "repository": {
                "pullRequest": {"reviewThreads": {"pageInfo": page, "nodes": nodes}}
            }
        }
    }


def _write_calls(calls):
    return [
        call
        for call in calls
        if "POST" in call or any("mutation(" in arg for arg in call)
    ]


@pytest.mark.parametrize("resolved", [False, True])
def test_reply_resolve_on_a_codex_thread(fake_gh, findings336, resolved):
    tmp, run = fake_gh
    threads = copy.deepcopy(findings336["threads"])
    codex = next(
        t for t in threads if t["comments"]["nodes"][0]["author"]["login"] == CODEX
    )
    codex["isResolved"] = resolved
    (tmp / "threads.json").write_text(json.dumps(_thread_page(threads)))
    (tmp / "body.txt").write_text("Fixed after verification.", encoding="utf-8")
    root_id = str(codex["comments"]["nodes"][0]["databaseId"])
    result, calls = run(
        "reply-resolve-thread.sh",
        "--pr",
        "336",
        "--repo",
        "IronbellyOrg/IronClaude",
        "--comment-id",
        root_id,
        "--body-file",
        str(tmp / "body.txt"),
    )
    assert result.returncode == 0, result.stderr
    writes = _write_calls(calls)
    if resolved:
        assert writes == []
        assert "idempotency_skip" in result.stdout
        return
    assert len(writes) == 2
    assert (
        f"repos/IronbellyOrg/IronClaude/pulls/336/comments/{root_id}/replies"
        in writes[0]
    )
    assert any("mutation(" in arg for arg in writes[1])
    assert f"threadId={codex['id']}" in writes[1]
    assert f"resolved thread {codex['id']}" in result.stdout


def test_retrigger_posts_the_codex_phrase(fake_gh):
    _, run = fake_gh
    result, calls = run(
        "retrigger-review.sh",
        "--pr",
        "336",
        "--repo",
        "IronbellyOrg/IronClaude",
        "--body",
        retrigger_phrase(CONTRACT, "codex"),
    )
    assert result.returncode == 0, result.stderr
    assert calls == [
        [
            "api",
            "--method",
            "POST",
            "repos/IronbellyOrg/IronClaude/issues/336/comments",
            "-f",
            "body=@codex review",
        ]
    ]


# --- 10. the SKILL snapshot gate and the A5 wording (design sections 14 and 18) -----

SKILL_MD = SCRIPTS.parent / "SKILL.md"


def _skill_gate(payload, *, pushed_sha=None, watermark=None, codex_watermark=None):
    text = SKILL_MD.read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    assert len(blocks) == 1, "keep one executable snapshot gate"
    namespace = {
        "payload": payload,
        "contract": CONTRACT,
        "pushed_sha": pushed_sha,
        "watermark": watermark,
        "codex_watermark": codex_watermark,
    }
    exec(compile(blocks[0], str(SKILL_MD), "exec"), namespace)
    return namespace


def test_skill_gate_adds_the_codex_part_on_the_same_snapshot(findings336):
    gated = _skill_gate(findings336)
    assert gated["codex_state"] == "findings"
    assert [f.reviewer for f in gated["codex_findings"]] == ["codex"] * 3
    assert gated["codex_routes"] == ["--fix"] * 3
    assert gated["activity"] == {"augment": True, "codex": True}
    assert gated["review_state"] == classify(findings336, CONTRACT)


def test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules(findings336):
    head = findings336["head_sha"]
    assert _skill_gate(findings336, pushed_sha="b" * 40)["codex_state"] == "polling"
    assert _skill_gate(findings336, pushed_sha=head)["codex_state"] == "polling"
    late = "2099-01-01T00:00:00Z"
    gated = _skill_gate(findings336, pushed_sha=head, codex_watermark=late)
    assert gated["codex_state"] == "polling" and gated["codex_findings"] == []


def test_skill_states_the_a5_rules():
    """A5: the SKILL text states the dedup, S5, fallback, event and resume rules."""
    text = SKILL_MD.read_text(encoding="utf-8")
    for fragment in (
        "dedup_groups(findings)",
        "routes at its members' highest remapped tier",
        "`fix_applied` is recorded for **every** member's `fix_key`",
        "**every verified member's thread** is replied to and resolved",
        '"flagged by: augment, codex"',
        "covers **only the reviewers re-triggered in this cycle**",
        "at least one\nre-triggered reviewer reaches `done`",
        'reviewer_incomplete{reviewer, phase: "rereview"}',
        "plus any merged Codex `findings`",
        'rebuild_state()["absent_reviewers"]',
        "pending_retriggers(",
        "rereview_requested{cycle_id, reviewer, timestamp}",
        "reuse the `cycle_id` of the dangling push record",
    ):
        assert fragment in text, fragment
    events = text[text.index("Every event that concerns one reviewer") :]
    events = events[: events.index("On `--resume`")]
    for name in (
        "poll_result",
        "review_detected",
        "findings_normalized",
        "finding_verified",
        "finding_unverified",
        "route_decision",
        "reply_posted",
        "thread_resolved",
        "rereview_requested",
    ):
        assert f"`{name}`" in events, name
    resume = text[text.index("**Resume of a re-triggered cycle:**") :]
    assert resume.index("pending_retriggers") < resume.index("before the S5 poll")
