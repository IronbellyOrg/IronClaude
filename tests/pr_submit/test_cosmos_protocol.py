"""Execute the attended protocol's documented gate against production helpers."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from unittest.mock import Mock

import pytest

import superclaude.pr_submit as core
from superclaude.pr_submit import classifier, severity_router
from superclaude.pr_submit.fsm import is_groundable
from tests.pr_submit.test_cosmos_poll import (
    adapter as adapter,
)
from tests.pr_submit.test_cosmos_poll import (
    config,
    connection,
    rest_item,
    thread,
)

SKILL = (
    Path(__file__).resolve().parents[2] / "src/superclaude/skills/sc-pr-submit-protocol"
)
HEAD = "13d246ec9e0d5aad4b6ea70529bebd9496a776e5"
WATERMARK = "2026-10-16T19:30:00Z"


def attended_gate(payload, *, pushed_sha=None, watermark=WATERMARK):
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    assert len(blocks) == 1, "keep one executable snapshot gate, not parallel parsers"
    namespace = {
        "payload": payload,
        "contract": core.DetectionContract.load(SKILL / "refs/detection-contract.md"),
        "pushed_sha": pushed_sha,
        "watermark": watermark,
        "codex_watermark": None,
    }
    exec(compile(blocks[0], str(SKILL / "SKILL.md"), "exec"), namespace)
    return namespace


def test_attended_gate_binds_actual_exports_and_same_context(load_fixture, monkeypatch):
    assert core.classify is classifier.classify
    assert core.actionable_finding_comments is classifier.actionable_finding_comments
    assert core.finding_from_comment is severity_router.finding_from_comment
    payload = load_fixture("cosmos-pr266.json")
    payload["threads"][0]["isResolved"] = False
    spies = {}
    for name in (
        "classify",
        "actionable_finding_comments",
        "finding_from_comment",
        "remap_severity",
        "route",
    ):
        spies[name] = Mock(wraps=getattr(core, name))
        monkeypatch.setattr(core, name, spies[name])
    gated = attended_gate(payload, pushed_sha=HEAD)
    assert gated["review_state"] == "findings"
    classification = spies["classify"].call_args
    selection = spies["actionable_finding_comments"].call_args
    assert classification == selection
    assert classification.args[0] is payload
    assert classification.kwargs == {
        "watermark": WATERMARK,
        "current_head_sha": HEAD,
    }
    for name in ("finding_from_comment", "remap_severity", "route"):
        spies[name].assert_called_once()
    finding = gated["findings"][0]
    assert (finding.comment_id, finding.thread_id, finding.review_id) == (
        4296483537,
        "PRRT_pr266_example",
        5550158176,
    )
    assert finding.line is None and finding.original_line == 172
    assert finding.is_outdated and finding.verification_status == "unverified"
    assert not is_groundable(finding)
    assert gated["routes"] == ["report-only"]


@pytest.mark.parametrize("resolved", [True, False])
def test_attended_gate_blocks_advanced_snapshot_before_head_override(
    load_fixture, monkeypatch, resolved
):
    payload = load_fixture("cosmos-pr266.json")
    payload["threads"][0]["isResolved"] = resolved
    payload["head_sha"] = "b" * 40  # complete snapshot after somebody else's push
    # The public override alone intentionally does NOT check actual snapshot head.
    contract = core.DetectionContract.load(SKILL / "refs/detection-contract.md")
    assert core.classify(payload, contract, current_head_sha=HEAD) == (
        "clean" if resolved else "findings"
    )
    spy = Mock(wraps=core.classify)
    monkeypatch.setattr(core, "classify", spy)
    gated = attended_gate(payload, pushed_sha=HEAD)
    spy.assert_not_called()
    assert gated["review_state"] == "polling"
    assert gated["findings"] == gated["routes"] == []


@pytest.mark.parametrize("watermark", [WATERMARK, "2026-10-16T20:00:00Z", "bad", None])
def test_attended_gate_requires_strict_time_attribution(load_fixture, watermark):
    gated = attended_gate(
        load_fixture("cosmos-pr266.json"), pushed_sha=HEAD, watermark=watermark
    )
    assert gated["review_state"] == ("clean" if watermark == WATERMARK else "polling")
    assert gated["findings"] == []


@pytest.mark.parametrize("flag", ["comments_ok", "reviews_ok", "threads_ok"])
def test_attended_gate_incomplete_sources_do_not_normalize(
    load_fixture, monkeypatch, flag
):
    payload = load_fixture("cosmos-pr266.json")
    payload[flag] = False
    spy = Mock(wraps=core.finding_from_comment)
    monkeypatch.setattr(core, "finding_from_comment", spy)
    gated = attended_gate(payload, pushed_sha=HEAD)
    assert gated["review_state"] == "polling"
    assert gated["findings"] == gated["routes"] == []
    spy.assert_not_called()


@pytest.mark.parametrize("signal", [{"has_findings": True}, {"findings_count": 1}])
def test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean(signal):
    payload = {
        "head_sha": HEAD,
        "reviews": [
            {
                "user": {"login": "augmentcode[bot]"},
                "state": "COMMENTED",
                "submitted_at": "2026-10-16T20:00:00Z",
                "commit_id": HEAD,
                **signal,
            }
        ],
        "comments": [],
    }
    contract = core.DetectionContract.load(SKILL / "refs/detection-contract.md")
    assert core.classify(payload, contract, watermark=WATERMARK) == "findings"
    assert (
        core.actionable_finding_comments(payload, contract, watermark=WATERMARK) == []
    )
    gated = attended_gate(payload, pushed_sha=HEAD)
    assert gated["review_state"] == "polling"
    assert gated["findings"] == gated["routes"] == []


def test_attended_gate_normalization_valueerror_discards_entire_batch(load_fixture):
    payload = load_fixture("cosmos-pr266.json")
    payload["threads"][0]["isResolved"] = False
    invalid = copy.deepcopy(payload["threads"][0])
    invalid["id"] += "2"
    invalid["comments"]["nodes"][0]["databaseId"] += 1
    invalid["comments"]["nodes"][0]["severity_hint"] = []
    payload["threads"].append(invalid)
    contract = core.DetectionContract.load(SKILL / "refs/detection-contract.md")
    selected = core.actionable_finding_comments(payload, contract, watermark=WATERMARK)
    assert len(selected) == 2
    with pytest.raises(ValueError):
        core.finding_from_comment(selected[-1])
    gated = attended_gate(payload, pushed_sha=HEAD)
    assert gated["review_state"] == "polling"
    assert gated["findings"] == gated["routes"] == []


def test_real_poll_to_documented_gate_preserves_later_root(adapter, load_fixture):
    """A16: real shell/JSON -> same selector -> adapter -> unchanged Low route."""
    snapshot = load_fixture("cosmos-pr266.json")
    last = copy.deepcopy(snapshot["threads"][0])
    last["isResolved"] = False
    data = config()
    data["reviews"] = [
        [{**rest_item(n), "user": {"login": "human"}} for n in range(1, 101)],
        [snapshot["reviews"][-1]],
    ]
    data["threads"] = [
        connection([thread(n, resolved=True) for n in range(1, 101)], more=True),
        connection([last], cursor="c2"),
    ]
    result, calls = adapter(data)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert core.poll_succeeded(payload)
    assert any("endCursor=c1" in call for call in calls)
    assert any("page=2" in call for call in calls)
    gated = attended_gate(payload, pushed_sha=HEAD)
    assert gated["review_state"] == "findings"
    assert len(gated["findings"]) == 1
    finding = gated["findings"][0]
    assert (finding.comment_id, finding.thread_id, finding.review_id) == (
        4296483537,
        "PRRT_pr266_example",
        5550158176,
    )
    assert finding.line is None and finding.original_line == 172
    assert finding.verification_status == "unverified"
    assert finding.remapped_severity is core.Severity.LOW
    assert gated["routes"] == ["report-only"]


def test_protocol_refs_pin_live_boundaries_and_existing_gates():
    required = {
        "SKILL.md": (
            "RunConfig.rereview_outcome",
            "optimistic legacy default",
            "evidence-validator",
            "without\nresetting elapsed time",
            'Never pass `review_state="findings"` with an empty `findings` list',
        ),
        "refs/detection-contract.md": (
            "not a stable\npublic API",
            "documentary fields, not runtime parser rules",
            "lower bound",
            "strictly\nnewer than `watermark`",
            "observed_at",
        ),
        "refs/augment-poll.md": (
            "reviews_ok",
            "comments_ok",
            "threads_ok",
            "comments(first:1)",
            "pageInfo{hasNextPage endCursor}",
            "all three flags false",
        ),
        "refs/review-retrigger.md": (
            'body="auggie review"',
            "payload.head_sha == pushed_sha",
            "RunConfig.rereview_outcome",
            "strictly newer",
            "observed_at",
        ),
        "refs/severity-routing.md": (
            "finding_from_comment(raw)",
            "ValueError",
            "LF or CRLF",
            'verification_status="unverified"',
            "evidence-validator",
        ),
        "refs/thread-reply.md": (
            "--thread-id",
            "no path/line lookalike match",
            "idempotency_skip BEFORE reply",
            "hasNextPage:false",
            "thread.isResolved:true",
        ),
    }
    for name, fragments in required.items():
        text = (SKILL / name).read_text(encoding="utf-8")
        for fragment in fragments:
            assert fragment in text, (name, fragment)
    contract = core.DetectionContract.load(SKILL / "refs/detection-contract.md")
    assert (contract.augment_bot_login, contract.augment_app_slug) == (
        "augmentcode[bot]",
        "augmentcode",
    )
    assert contract.accepted_trigger_phrases[0] == "auggie review"
