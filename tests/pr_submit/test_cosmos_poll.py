"""Exercise the real shell adapters with an executable, write-isolated gh stub."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from superclaude.pr_submit import DetectionContract, classify

SCRIPTS = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-pr-submit-protocol/scripts"
)
HEAD = "13d246ec9e0d5aad4b6ea70529bebd9496a776e5"
OTHER_HEAD = "0f5fef56e1abf1958708473f2004c5627a0a163d"
REPO = "acme/widgets"


def rest_item(number=55):
    return {
        "id": number,
        "commit_id": HEAD,
        "submitted_at": "2026-10-16T20:10:00Z",
        "state": "COMMENTED",
        "body": "review body",
        "user": {"login": "augmentcode[bot]"},
    }


def root(number=1):
    return {
        "id": f"PRRC_{number}",
        "databaseId": number,
        "body": "A finding\n**Severity:** low",
        "path": "a.py",
        "line": None,
        "originalLine": 172,
        "createdAt": "2026-10-16T20:00:00Z",
        "author": {"login": "augmentcode"},
        "replyTo": None,
        "pullRequestReview": {
            "id": "PRR_55",
            "databaseId": 55,
            "commit": {"oid": OTHER_HEAD},
        },
    }


def thread(number=1, *, resolved=False):
    return {
        "id": f"PRRT_{number}",
        "path": "a.py",
        "line": None,
        "originalLine": 172,
        "isResolved": resolved,
        "isOutdated": True,
        "comments": {"nodes": [root(number)]},
    }


def connection(nodes, *, more=False, cursor="c1", head=HEAD):
    return {
        "data": {
            "repository": {
                "pullRequest": {
                    "headRefOid": head,
                    "reviewThreads": {
                        "pageInfo": {"hasNextPage": more, "endCursor": cursor},
                        "nodes": nodes,
                    },
                }
            }
        }
    }


def config():
    return {
        "heads": [HEAD, HEAD],
        "reviews": [[]],
        "issue": [[]],
        "inline": [[]],
        "threads": [connection([], cursor=None)],
        "cursor_pages": {"c1": 1, "c2": 2},
        "reply": {"id": 999, "in_reply_to_id": 101},
        "resolve": {
            "data": {
                "resolveReviewThread": {
                    "thread": {"id": "PRRT_101", "isResolved": True}
                }
            }
        },
    }


@pytest.fixture
def adapter(tmp_path):
    gh = tmp_path / "gh"
    gh.write_text(
        r"""#!/usr/bin/env bash
set -euo pipefail
jq -nc --args '$ARGS.positional' -- "$@" >> "$STUB_DIR/calls.jsonl"
CFG="$STUB_DIR/config.json"
OUT="$STUB_DIR/response.json"
field() {
    local name="$1" arg
    for arg in "${@:2}"; do
        if [[ "$arg" == "$name="* ]]; then printf '%s' "${arg#*=}"; return; fi
    done
}
emit() {
    jq -c "$@" "$CFG" > "$OUT"
    local code
    code="$(jq -r 'if type == "object" then ._exit // 0 else 0 end' "$OUT")"
    if jq -e 'type == "object" and has("_raw")' "$OUT" >/dev/null; then
        jq -r '._raw' "$OUT"
    else
        cat "$OUT"
    fi
    exit "$code"
}
if [ "$1" = pr ]; then
    [[ " $* " == *" --repo acme/widgets "* ]] || exit 91
    n=0
    if [ -f "$STUB_DIR/pr-count" ]; then read -r n < "$STUB_DIR/pr-count"; fi
    printf '%s\n' "$((n+1))" > "$STUB_DIR/pr-count"
    emit --argjson n "$n" '.heads[$n] | if type == "object" then . else
        {number:266,url:"https://example.test/pr/266",headRefName:"fix/x",headRefOid:.,baseRefName:"master"} end'
fi
[ "$1" = api ] || exit 92
if [[ " $* " == *" --method POST "* ]]; then
    [[ " $* " == *" repos/acme/widgets/pulls/266/comments/"*"/replies "* ]] || exit 93
    input=""
    while [ $# -gt 0 ]; do
        if [ "$1" = --input ]; then input="$2"; break; fi
        shift
    done
    jq -e '.body == "Fixed after verification."' "$input" >/dev/null
    emit '.reply'
fi
if [ "$2" = graphql ]; then
    query="$(field query "$@")"
    if [[ "$query" == *'mutation('* ]]; then
        [[ "$(field threadId "$@")" == PRRT_101 ]] || exit 94
        emit '.resolve'
    fi
    [[ "$(field owner "$@")" == acme && "$(field repo "$@")" == widgets && "$(field pr "$@")" == 266 ]] || exit 95
    [[ "$query" == *'reviewThreads(first:100,after:$endCursor)'* && "$query" == *'comments(first:1)'* && "$query" == *'pageInfo{hasNextPage endCursor}'* ]] || exit 96
    [[ "$query" != *'comments(first:100)'* ]] || exit 97
    cursor="$(field endCursor "$@")"
    emit --arg cursor "$cursor" '.threads[if $cursor == "" then 0 else .cursor_pages[$cursor] // 999 end]'
fi
[[ " $* " == *" --method GET "* && " $* " == *" per_page=100 "* && " $* " != *" --paginate "* ]] || exit 98
page="$(field page "$@")"
case "$2" in
    repos/acme/widgets/pulls/266/reviews) kind=reviews ;;
    repos/acme/widgets/issues/266/comments) kind=issue ;;
    repos/acme/widgets/pulls/266/comments) kind=inline ;;
    *) exit 99 ;;
esac
emit --arg kind "$kind" --argjson page "$page" '.[$kind][$page-1]'
""",
        encoding="utf-8",
    )
    gh.chmod(0o755)
    (tmp_path / "body.txt").write_text("Fixed after verification.", encoding="utf-8")

    def run(data, *, reply=False, extra=()):
        (tmp_path / "config.json").write_text(json.dumps(data), encoding="utf-8")
        script = "reply-resolve-thread.sh" if reply else "poll-augment-review.sh"
        args = [str(SCRIPTS / script), "--pr", "266", "--repo", REPO]
        if reply:
            args += ["--comment-id", "101", "--body-file", str(tmp_path / "body.txt")]
        result = subprocess.run(
            [*args, *extra],
            capture_output=True,
            text=True,
            timeout=30,
            env={
                **os.environ,
                "PATH": f"{tmp_path}:{os.environ['PATH']}",
                "STUB_DIR": str(tmp_path),
            },
        )
        calls = [
            json.loads(line)
            for line in (tmp_path / "calls.jsonl").read_text().splitlines()
        ]
        return result, calls

    return run


def assert_poll(result, **flags):
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.splitlines()) == 1
    payload = json.loads(result.stdout)
    assert payload["head_sha"] == HEAD
    assert len(payload["observed_at"]) == 20
    assert payload["observed_at"].endswith("Z")
    for name in ("reviews_ok", "comments_ok", "threads_ok"):
        assert payload[name] is flags.get(name, True), (name, payload, result.stderr)
    if not all(payload[name] for name in ("reviews_ok", "comments_ok", "threads_ok")):
        assert payload["state"] == "polling"
    return payload


def test_poll_all_pages_and_raw_provenance(adapter):
    data = config()
    review = {
        "id": 55,
        "commit_id": HEAD,
        "submitted_at": "2026-10-16T20:10:00Z",
        "state": "COMMENTED",
        "body": "review body",
        "user": {"login": "augmentcode[bot]"},
    }
    data["reviews"] = [
        [{**review, "id": n} for n in range(1, 101)],
        [{**review, "id": 101}],
    ]
    for kind in ("issue", "inline"):
        data[kind] = [[rest_item(n) for n in range(1, 101)], [rest_item(101)]]
    data["threads"] = [
        connection([thread(n) for n in range(1, 101)], more=True),
        connection([thread(101)], cursor="c2"),
    ]
    result, calls = adapter(data)
    payload = assert_poll(result)
    assert payload["reviews"][-1] == {**review, "id": 101}
    assert len(payload["comments"]) == 202
    assert len(payload["threads"]) == 101
    assert payload["threads"][-1] == thread(101)
    assert any("endCursor=c1" in call for call in calls)
    assert payload["state"] == "review_present"


@pytest.mark.parametrize(
    "login,expected",
    [
        ("operator", "clean"),
        ("other-bot[bot]", "clean"),
        ("augmentcode[bot]", "polling"),
    ],
)
@pytest.mark.parametrize("timestamp", ["absent", None])
def test_pending_drafts_preserve_transport_and_author_gates(
    adapter, load_fixture, login, expected, timestamp
):
    snapshot = load_fixture("cosmos-pr266.json")
    draft = {**rest_item(999), "state": "PENDING", "user": {"login": login}}
    if timestamp == "absent":
        draft.pop("submitted_at")
    else:
        draft["submitted_at"] = timestamp
    data = config()
    data["reviews"] = [snapshot["reviews"] + [draft]]
    data["threads"] = [connection(snapshot["threads"])]
    result, _ = adapter(data)
    payload = assert_poll(result)
    assert payload["reviews"][-1] == draft
    assert classify(payload, DetectionContract.for_arming()) == expected


@pytest.mark.parametrize(
    "state,timestamp",
    [
        ("COMMENTED", "absent"),
        ("PENDING", 123),
        ("PENDING", {}),
        ("PENDING", []),
        ("PENDING", False),
    ],
)
def test_review_timestamp_presence_and_type_still_fail_closed(
    adapter, state, timestamp
):
    review = {**rest_item(), "state": state}
    if timestamp == "absent":
        review.pop("submitted_at")
    else:
        review["submitted_at"] = timestamp
    data = config()
    data["reviews"] = [[review]]
    result, _ = adapter(data)
    payload = assert_poll(result, reviews_ok=False)
    assert classify(payload, DetectionContract.for_arming()) == "polling"


@pytest.mark.parametrize(
    "kind,flag",
    [("reviews", "reviews_ok"), ("issue", "comments_ok"), ("inline", "comments_ok")],
)
@pytest.mark.parametrize(
    "bad",
    [
        {"message": "rate limited"},
        None,
        {"_raw": "not json"},
        {"_exit": 1},
        [None],
        [{"body": "missing ID"}],
        {"_raw": "[]\n[]"},
    ],
)
def test_rest_malformed_and_failures(adapter, kind, flag, bad):
    data = config()
    data[kind] = [bad]
    result, _ = adapter(data)
    assert_poll(result, **{flag: False})


@pytest.mark.parametrize(
    "kind,flag",
    [("reviews", "reviews_ok"), ("issue", "comments_ok"), ("inline", "comments_ok")],
)
def test_rest_later_page_failure_and_repeated_page(adapter, kind, flag):
    data = config()
    first = [rest_item(n) for n in range(1, 101)]
    data[kind] = [first, {"_exit": 1}]
    result, calls = adapter(data)
    assert_poll(result, **{flag: False})
    assert any("page=2" in call for call in calls)


BAD_THREADS = [
    {"errors": [{"message": "denied"}], **connection([])},
    {"data": {"repository": None}},
    {"data": {"repository": {"pullRequest": None}}},
    {"data": {"repository": {"pullRequest": {"headRefOid": HEAD}}}},
    connection([], more=True, cursor=None),
    connection([thread()], more=True, cursor=None),
    connection([thread()], cursor=None),
    connection([thread()], head=OTHER_HEAD),
    {"_raw": "{}\n{}"},
    {"_raw": "malformed"},
    {"_exit": 1},
]


@pytest.mark.parametrize("bad", BAD_THREADS)
def test_poll_invalid_threads(adapter, bad):
    data = config()
    data["threads"] = [bad]
    result, _ = adapter(data)
    payload = assert_poll(result, threads_ok=False)
    assert payload["threads"] == []


@pytest.mark.parametrize(
    "bad",
    [
        {"errors": [{"message": "later-page failure"}]},
        {"_exit": 1},
        connection([thread(101)], more=True, cursor="c1"),
        connection([thread(101)], cursor="c1"),
        connection([], cursor=None),
        connection([thread(1)], cursor="c2"),
    ],
)
def test_poll_later_thread_failure_or_invalid_completion(adapter, bad):
    data = config()
    data["threads"] = [connection([thread()], more=True), bad]
    result, calls = adapter(data)
    assert_poll(result, threads_ok=False)
    assert len([call for call in calls if "graphql" in call]) == 2


@pytest.mark.parametrize(
    "field,value",
    [
        ("nodes", None),
        ("nodes", {}),
        ("nodes", [None]),
        ("pageInfo", None),
        ("pageInfo", {"hasNextPage": "false", "endCursor": None}),
        ("pageInfo", {"hasNextPage": False}),
    ],
)
def test_thread_connection_shape(adapter, field, value):
    data = config()
    data["threads"][0]["data"]["repository"]["pullRequest"]["reviewThreads"][field] = (
        value
    )
    result, _ = adapter(data)
    assert_poll(result, threads_ok=False)


def test_poll_changed_head_invalidates_entire_snapshot(adapter):
    data = config()
    data["heads"][-1] = OTHER_HEAD
    result, _ = adapter(data)
    assert_poll(result, reviews_ok=False, comments_ok=False, threads_ok=False)


@pytest.mark.parametrize("bad", [{"_exit": 1}, {"_raw": "not json"}, None, "short-sha"])
def test_poll_initial_metadata_failure_is_one_incomplete_event(adapter, bad):
    data = config()
    data["heads"][0] = bad
    result, calls = adapter(data)
    assert result.returncode == 0
    assert len(result.stdout.splitlines()) == 1
    payload = json.loads(result.stdout)
    assert payload["state"] == "polling"
    assert not any(
        payload[flag] for flag in ("reviews_ok", "comments_ok", "threads_ok")
    )
    assert len(calls) == 1


def write_calls(calls):
    return [
        call
        for call in calls
        if "POST" in call or any("mutation(" in arg for arg in call)
    ]


@pytest.mark.parametrize("resolved", [False, True])
@pytest.mark.parametrize("known_thread", [False, True])
def test_reply_later_page_and_already_resolved(adapter, resolved, known_thread):
    data = config()
    data["threads"] = [
        connection([thread(n) for n in range(1, 101)], more=True),
        connection([thread(101, resolved=resolved)], cursor="c2"),
    ]
    extra = ("--thread-id", "PRRT_101") if known_thread else ()
    result, calls = adapter(data, reply=True, extra=extra)
    assert result.returncode == 0, result.stderr
    writes = write_calls(calls)
    if resolved:
        assert not writes
        assert "idempotency_skip" in result.stdout
    else:
        assert len(writes) == 2
        assert "POST" in writes[0]
        assert any("mutation(" in arg for arg in writes[1])
        assert (
            len([call for call in calls[: calls.index(writes[0])] if "graphql" in call])
            == 2
        )


@pytest.mark.parametrize("known_thread", ["PRRT_1", "PRRT_missing"])
@pytest.mark.parametrize("resolved", [False, True])
def test_reply_known_thread_missing_or_conflicting_never_falls_back(
    adapter, known_thread, resolved
):
    data = config()
    data["threads"] = [connection([thread(1, resolved=resolved), thread(101)])]
    result, calls = adapter(data, reply=True, extra=("--thread-id", known_thread))
    assert result.returncode != 0
    assert write_calls(calls) == []
    assert "idempotency_skip" not in result.stdout


@pytest.mark.parametrize("bad", BAD_THREADS[:7] + [{"_exit": 1}, {"_raw": "bad"}])
def test_reply_invalid_lookup_never_writes(adapter, bad):
    data = config()
    data["threads"] = [bad]
    result, calls = adapter(data, reply=True)
    assert result.returncode != 0
    assert write_calls(calls) == []


@pytest.mark.parametrize(
    "bad",
    [
        connection([thread(101)], cursor="c1"),
        {"errors": [{"message": "no"}]},
        connection([thread(101)], cursor=None),
        connection([thread(101)], more=True, cursor="c1"),
    ],
)
def test_reply_incomplete_later_page_never_writes(adapter, bad):
    data = config()
    data["threads"] = [connection([thread(101)], more=True), bad]
    result, calls = adapter(data, reply=True)
    assert result.returncode != 0
    assert write_calls(calls) == []


def test_reply_missing_identity_does_not_resolve_path_line_lookalike(adapter):
    data = config()
    data["threads"] = [connection([thread(1)])]
    result, calls = adapter(data, reply=True, extra=("--path", "a.py", "--line", "172"))
    assert result.returncode != 0
    assert write_calls(calls) == []


def test_reply_duplicate_root_identity_never_writes(adapter):
    data = config()
    other = thread(102)
    other["comments"]["nodes"] = [root(101)]
    data["threads"] = [connection([thread(101), other])]
    result, calls = adapter(data, reply=True)
    assert result.returncode != 0
    assert write_calls(calls) == []


@pytest.mark.parametrize(
    "bad",
    [
        {"message": "denied"},
        {"id": 999, "in_reply_to_id": 102},
        {"_raw": "bad"},
        {"_exit": 1},
    ],
)
def test_reply_invalid_post_response_never_resolves(adapter, bad):
    data = config()
    data["threads"] = [connection([thread(101)])]
    data["reply"] = bad
    result, calls = adapter(data, reply=True)
    assert result.returncode != 0
    assert len(write_calls(calls)) == 1


@pytest.mark.parametrize(
    "bad",
    [
        {"errors": [{"message": "denied"}]},
        {"data": None},
        {
            "data": {
                "resolveReviewThread": {"thread": {"id": "other", "isResolved": True}}
            }
        },
        {
            "data": {
                "resolveReviewThread": {
                    "thread": {"id": "PRRT_101", "isResolved": False}
                }
            }
        },
        {"_raw": "bad"},
        {"_exit": 1},
    ],
)
def test_reply_validates_mutation_not_just_exit_code(adapter, bad):
    data = config()
    data["threads"] = [connection([thread(101)])]
    data["resolve"] = bad
    result, calls = adapter(data, reply=True)
    assert result.returncode == 3
    assert len(write_calls(calls)) == 2


@pytest.mark.parametrize("resolved", [False, True])
def test_no_resolve_still_checks_idempotency(adapter, resolved):
    data = config()
    data["threads"] = [connection([thread(101, resolved=resolved)])]
    result, calls = adapter(data, reply=True, extra=("--no-resolve",))
    assert result.returncode == 0, result.stderr
    assert len(write_calls(calls)) == (0 if resolved else 1)
