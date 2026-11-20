"""Task 12: the result comment and the Status move (``complete.py``), over a fake runner."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_pipeline import complete
from superclaude.cli.issue_watch import predicates
from superclaude.cli.issue_watch.runner import CommandResult

REPO = "IronbellyOrg/IronClaude"
ISSUE = 9
PROJECT = "PVT_cfg"
OTHER_PROJECT = "PVT_other"
RUN = 4242
OWN = "coord-login"
IN_REVIEW_ID = "opt-in-review"
OPTIONS = [
    {"id": "opt-research", "name": "Research"},
    {"id": "opt-done", "name": "Done"},
    {"id": IN_REVIEW_ID, "name": "In review"},
]
CANARY = "CANARY-12-NO-ECHO"


def node(
    item_id: str = "PVTI_cfg",
    project: str = PROJECT,
    status: str | None = "Plan",
    *,
    archived: bool = False,
    options: list[dict] | None = None,
) -> dict:
    return {
        "id": item_id,
        "isArchived": archived,
        "project": {
            "id": project,
            "field": {
                "id": "PVTSSF_status",
                "options": OPTIONS if options is None else options,
            },
        },
        "status": {"name": status} if status is not None else None,
    }


def ok(stdout: str = "") -> CommandResult:
    return CommandResult(("gh",), 0, stdout, "", False, None, 0.0)


def bad() -> CommandResult:
    return CommandResult(("gh",), 1, "", "boom", False, None, 0.0)


class World:
    """A scripted ``gh`` for one issue: its Project items, comments and the writes made."""

    def __init__(self, *nodes: dict) -> None:
        self.nodes = list(nodes) if nodes else [node()]
        self.comments: list[dict] = []  # {login, body}
        self.argvs: list[list[str]] = []
        self.posts: list[str] = []
        self.mutations: list[list[str]] = []
        self.fail_move = False
        self.fail_post = False

    def other_comment(self, login: str, body: str) -> None:
        self.comments.append({"login": login, "body": body})

    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
        self.argvs.append(list(argv))
        if argv[:3] == ["gh", "api", "user"]:
            return ok(OWN + "\n")
        if argv[:3] == ["gh", "api", "graphql"]:
            query = next(a for a in argv if a.startswith("query="))
            if "mutation" in query:
                self.mutations.append(list(argv))
                return bad() if self.fail_move else ok('{"data": {}}')
            return ok(
                json.dumps(
                    {
                        "data": {
                            "repository": {
                                "issue": {
                                    "projectItems": {
                                        "nodes": self.nodes,
                                        "pageInfo": {
                                            "hasNextPage": False,
                                            "endCursor": None,
                                        },
                                    }
                                }
                            }
                        }
                    }
                )
            )
        if "POST" in argv:
            assert argv[argv.index("POST") - 1] == "--method"
            if self.fail_post:
                return bad()
            body = next(a for a in argv if a.startswith("body="))[len("body=") :]
            self.posts.append(body)
            self.comments.append({"login": OWN, "body": body})
            return ok("{}")
        assert argv[2:4] == ["--method", "GET"], argv
        page = int(next(a for a in argv if a.startswith("page="))[len("page=") :])
        jq = argv[argv.index("--jq") + 1]
        marker = json.loads(re.search(r"contains\((\".*\")\)", jq).group(1))
        rows = [
            {"login": c["login"], "marker": marker in c["body"]} for c in self.comments
        ]
        return ok(json.dumps(rows if page == 1 else []))


def call(
    world: World,
    outcome: str = "succeeded",
    *,
    run_id: int = RUN,
    summary: object = None,
    **over,
) -> str:
    args = {
        "repo": REPO,
        "issue": ISSUE,
        "project_id": PROJECT,
        "run_id": run_id,
        "outcome": outcome,
        "summary_path": summary,
    }
    args.update(over)
    return complete.complete(runner=world, **args)


def moved_option(world: World) -> str:
    argv = world.mutations[0]
    return next(a for a in argv if a.startswith("optionId="))[len("optionId=") :]


def test_succeeded_posts_one_comment_and_moves_the_status_to_in_review() -> None:
    world = World(node(status="Plan"))
    assert call(world) == complete.COMPLETED
    assert len(world.posts) == 1 and len(world.mutations) == 1
    assert moved_option(world) == IN_REVIEW_ID
    assert "itemId=PVTI_cfg" in world.mutations[0]
    assert f"projectId={PROJECT}" in world.mutations[0]
    assert "fieldId=PVTSSF_status" in world.mutations[0]


@pytest.mark.parametrize("status", predicates.ALLOWED_STATUSES)
def test_every_allowed_status_ends_at_in_review(status: str) -> None:
    world = World(node(status=status))
    assert call(world) == complete.COMPLETED
    assert moved_option(world) == IN_REVIEW_ID


def test_the_end_status_table_is_keyed_by_exactly_the_allowed_statuses() -> None:
    assert tuple(complete.END_STATUS) == predicates.ALLOWED_STATUSES
    assert set(complete.END_STATUS.values()) == {"In review"}


@pytest.mark.parametrize("outcome", ["failed", "blocked", "partial"])
def test_other_outcomes_post_a_comment_and_never_move_the_status(outcome: str) -> None:
    world = World(node(status="Plan"))
    assert call(world, outcome) == complete.COMMENTED
    assert len(world.posts) == 1 and world.mutations == []
    assert f"Result of the run: {outcome}" in world.posts[0]
    # no Project read is needed for a non-moving outcome
    assert not any("projectItems" in " ".join(a) for a in world.argvs)


def test_an_issue_on_two_projects_uses_the_configured_project_and_its_item() -> None:
    world = World(
        node("PVTI_other", OTHER_PROJECT, "Plan"), node("PVTI_cfg", PROJECT, "Plan")
    )
    assert call(world) == complete.COMPLETED
    assert "itemId=PVTI_cfg" in world.mutations[0]
    assert f"projectId={PROJECT}" in world.mutations[0]
    assert "itemId=PVTI_other" not in world.mutations[0]


def test_zero_items_in_the_project_are_refused_with_no_write() -> None:
    world = World(node("PVTI_other", OTHER_PROJECT, "Plan"))
    assert call(world) == "refused:project_missing"
    assert world.posts == [] and world.mutations == []


def test_an_archived_item_does_not_count() -> None:
    world = World(node("PVTI_old", PROJECT, "Plan", archived=True))
    assert call(world) == "refused:project_missing"
    world = World(node("PVTI_old", PROJECT, "Plan", archived=True), node("PVTI_new"))
    assert call(world) == complete.COMPLETED
    assert "itemId=PVTI_new" in world.mutations[0]


def test_two_live_items_in_the_project_are_refused_with_no_write() -> None:
    world = World(node("PVTI_a"), node("PVTI_b"))
    assert call(world) == "refused:project_ambiguous"
    assert world.posts == [] and world.mutations == []


def test_a_status_field_without_an_in_review_option_is_refused_with_no_write() -> None:
    world = World(node(options=OPTIONS[:2]))
    assert call(world) == "refused:status_option_missing"
    assert world.posts == [] and world.mutations == []
    world = World(node(options=[]))
    assert call(world) == "refused:status_option_missing"
    assert world.posts == [] and world.mutations == []


@pytest.mark.parametrize("status", ["Done", "Backlog", "In progress", None])
def test_a_status_a_person_moved_gets_the_comment_and_no_mutation(
    status: str | None,
) -> None:
    world = World(node(status=status))
    assert call(world) == complete.STATUS_MOVED_BY_PERSON
    assert len(world.posts) == 1 and world.mutations == []


def test_a_second_call_for_the_same_run_posts_no_second_comment() -> None:
    world = World(node(status="Plan"))
    assert call(world, "failed") == complete.COMMENTED
    assert call(world, "failed") == complete.COMMENTED
    assert len(world.posts) == 1


def test_another_run_id_does_not_suppress_the_comment() -> None:
    world = World()
    call(world, "failed", run_id=4242)
    call(
        world, "failed", run_id=42420
    )  # 4242 is a prefix of 42420: still its own marker
    call(world, "failed", run_id=4243)
    assert len(world.posts) == 3


def test_a_marker_posted_by_another_login_does_not_suppress_the_comment() -> None:
    world = World()
    world.other_comment("someone-else", complete.result_marker(ISSUE, RUN))
    assert call(world, "failed") == complete.COMMENTED
    assert len(world.posts) == 1


def test_a_failed_first_move_is_retried_by_the_second_call() -> None:
    world = World(node(status="Plan"))
    world.fail_move = True
    assert call(world) == "failed:status_move"
    assert len(world.posts) == 1 and len(world.mutations) == 1  # the comment stays
    world.fail_move = False
    assert call(world) == complete.COMPLETED
    assert len(world.posts) == 1  # no second comment
    assert len(world.mutations) == 2


def test_a_call_after_a_successful_move_changes_nothing() -> None:
    world = World(node(status="In review"))
    assert call(world) == complete.COMPLETED
    assert world.mutations == []


def test_a_graphql_error_in_a_200_reply_is_a_failed_move() -> None:
    world = World(node(status="Plan"))
    real = world.run

    def run(argv, timeout, *, cwd=None):
        if argv[:3] == ["gh", "api", "graphql"] and any(
            a.startswith("query=mutation") for a in argv
        ):
            world.mutations.append(list(argv))
            return ok('{"errors": [{"message": "no"}]}')
        return real(argv, timeout, cwd=cwd)

    world.run = run  # type: ignore[method-assign]
    assert call(world) == "failed:status_move"
    assert len(world.posts) == 1


def test_a_failed_comment_post_moves_nothing() -> None:
    world = World(node(status="Plan"))
    world.fail_post = True
    assert call(world) == "failed:comment_post"
    assert world.mutations == []


@pytest.mark.parametrize(
    "over,word",
    [
        ({"outcome": "done"}, "refused:bad_outcome"),
        ({"outcome": None}, "refused:bad_outcome"),
        ({"outcome": "Succeeded"}, "refused:bad_outcome"),
        ({"issue": 0}, "refused:bad_issue"),
        ({"issue": "9"}, "refused:bad_issue"),
        ({"issue": True}, "refused:bad_issue"),
        ({"issue": 10**9}, "refused:bad_issue"),
        ({"project_id": "PVT_x; rm"}, "refused:bad_project_id"),
        ({"project_id": "PVT_"}, "refused:bad_project_id"),
        ({"project_id": "PVT_cfg\n"}, "refused:bad_project_id"),
        ({"project_id": None}, "refused:bad_project_id"),
        ({"repo": "SuperClaude-Org"}, "refused:bad_repo"),
        ({"repo": "a/b/c"}, "refused:bad_repo"),
        ({"repo": "a/b c"}, "refused:bad_repo"),
        ({"repo": "{owner}/{repo}"}, "refused:bad_repo"),
        ({"repo": None}, "refused:bad_repo"),
        ({"run_id": 0}, "refused:bad_run"),
        ({"run_id": "4242"}, "refused:bad_run"),
        ({"run_id": True}, "refused:bad_run"),
    ],
)
def test_bad_inputs_are_refused_before_any_call(over: dict, word: str) -> None:
    world = World()
    assert call(world, **over) == word
    assert world.argvs == []


def test_the_marker_never_contains_the_claim_marker() -> None:
    marker = complete.result_marker(ISSUE, RUN)
    assert marker == "<!-- sc:issue:result issue=9 run=4242 -->"
    assert predicates.CLAIM_MARKER not in marker
    world = World()
    call(world, "failed")
    assert predicates.CLAIM_MARKER not in world.posts[0]
    assert world.posts[0].startswith(marker)


def test_the_comment_holds_only_the_outcome_artifacts_and_pull_request(
    tmp_path: Path,
) -> None:
    summary = tmp_path / "result.md"
    summary.write_text(
        "outcome: succeeded\nartifacts: .dev/issues/9/a.md, docs/b.md\npull_request: 12\n"
    )
    world = World(node(status="Plan"))
    assert call(world, summary=str(summary)) == complete.COMPLETED
    assert world.posts[0].splitlines()[1:] == [
        "Result of the run: succeeded",
        "Artifacts: .dev/issues/9/a.md, docs/b.md",
        "Pull request: #12",
    ]
    bare = World()
    call(bare, "failed")
    assert bare.posts[0].splitlines()[2:] == ["Artifacts: none", "Pull request: none"]


def test_a_result_file_outcome_that_differs_from_the_outcome_argument_is_refused(
    tmp_path: Path,
) -> None:
    summary = tmp_path / "result.md"
    summary.write_text("outcome: failed\nartifacts: none\npull_request: none\n")
    world = World(node(status="Plan"))
    assert call(world, "succeeded", summary=str(summary)) == "refused:bad_summary"
    assert world.posts == [] and world.mutations == []


@pytest.mark.parametrize(
    "text",
    [
        "",
        "outcome: failed\n",
        f"outcome: failed\nartifacts: {CANARY} and more\npull_request: none\n",
        "outcome: failed\nartifacts: ../etc/passwd\npull_request: none\n",
        "outcome: failed\nartifacts: a.md\npull_request: 0\n",
        "outcome: failed\nartifacts: a.md\npull_request: #5\n",
        "artifacts: a.md\noutcome: failed\npull_request: none\n",
        "outcome: failed\nartifacts: a.md\npull_request: none\nextra: x\n",
        "outcome: failed\nartifacts: "
        + ", ".join(f"f{i}" for i in range(21))
        + "\npull_request: none\n",
    ],
)
def test_a_malformed_result_file_is_refused_with_no_call_and_nothing_echoed(
    tmp_path: Path, text: str
) -> None:
    summary = tmp_path / "result.md"
    summary.write_text(text)
    world = World()
    assert call(world, "failed", summary=str(summary)) == "refused:bad_summary"
    assert world.argvs == []
    assert call(world, "failed", summary=str(tmp_path / "missing.md")) == (
        "refused:bad_summary"
    )


def test_every_result_is_a_closed_word_and_no_text_is_echoed(tmp_path: Path) -> None:
    summary = tmp_path / "result.md"
    summary.write_text("outcome: failed\nartifacts: a.md\npull_request: none\n")
    words = set()
    for status in ("Plan", "Done", "In review"):
        words.add(call(World(node(status=status))))
    words.add(call(World(), "failed", summary=str(summary)))
    words.add(call(World(), "bogus"))
    assert words <= complete.RESULT_WORDS
    assert all(CANARY not in w for w in words)


def test_the_coordinators_own_comment_leaves_unchanged_since_clean() -> None:
    """Comments by the watcher's own login are skipped, so the result comment voids nothing."""
    at = lambda s: datetime(2026, 11, 16, 10, s, 0, tzinfo=timezone.utc)  # noqa: E731
    approved_at = at(10)
    own = predicates.CommentEdit(1, OWN, at(30), at(31))
    edits = predicates.EditEvidence(at(0), None, (own,))
    assert predicates.unchanged_since(approved_at, edits, [], own_login=OWN) is None
    other = predicates.CommentEdit(2, "stranger", at(30), None)
    edits = predicates.EditEvidence(at(0), None, (own, other))
    assert (
        predicates.unchanged_since(approved_at, edits, [], own_login=OWN)
        == "edited_after_approval"
    )


def test_the_module_writes_only_through_the_two_gh_forms_it_names() -> None:
    world = World(node(status="Plan"))
    call(world)
    writes = [
        a
        for a in world.argvs
        if "POST" in a or any(x.startswith("query=mutation") for x in a)
    ]
    assert len(writes) == 2
    post = next(a for a in writes if "POST" in a)
    assert post[:4] == ["gh", "api", "--method", "POST"]
    assert post[4] == f"repos/{REPO}/issues/{ISSUE}/comments"
