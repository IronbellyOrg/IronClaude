"""The refusal of the orchestrator as a control plane (design 5.9, rows N2 to N7).

``refuse`` has a failing case for every pattern of the table, a passing case for
the ordinary commands each wave runs, and the table of the design is compared with
the data of ``limits.py`` in both directions.
"""

from __future__ import annotations

import json
import os
import re
import shlex
from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from superclaude.cli.issue_watch import github
from superclaude.cli.issue_watch.runner import CommandResult
from superclaude.cli.orchestrator import common, limits
from superclaude.cli.orchestrator.limits import (
    ARGV_INVALID,
    RULE_ROWS,
    RULES,
    GuardedRunner,
    Refused,
    refuse,
)

ANSWER_REF = "answer:2026-11-19T10:00:00Z#merge_safety"
# The design is at docs/designs/orchestrator.md on master; the comparison with the table
# of 5.9 skips only when that file is missing (a branch cut before it landed).
# ORCHESTRATOR_SPEC_PATH points the test at another copy.
SPEC = Path(
    os.environ.get("ORCHESTRATOR_SPEC_PATH")
    or Path(__file__).resolve().parents[2] / "docs/designs/orchestrator.md"
)
ESC = "\x1b"
ETX = "\x03"


def argv(line: str) -> list[str]:
    return shlex.split(line)


# (argv, reason code): every argv named in the row "PR B: limits (5.9)" of the design
# (9.1), then the other forms each pattern has.
REFUSED = [
    # N2
    ("git push origin --delete x", "n2_git_push_delete"),
    ("git push -d origin x", "n2_git_push_delete"),
    ("git push origin :x", "n2_git_push_delete"),
    # shared branch history: force pushes and a GraphQL ref deletion (owner ruling, Q3 and Q4)
    ("git push --force origin main", "n2_git_push_force"),
    ("git push origin main --force", "n2_git_push_force"),
    ("git push --force-with-lease origin main", "n2_git_push_force"),
    ("git push --force-with-lease=main:abc1234 origin main", "n2_git_push_force"),
    ("git push --force-if-includes origin main", "n2_git_push_force"),
    ("git push -f origin main", "n2_git_push_force"),
    ("git push -fu origin main", "n2_git_push_force"),
    ("git push origin +main", "n2_git_push_force"),
    ("git push origin +HEAD:refs/heads/main", "n2_git_push_force"),
    ("git push --mirror origin", "n2_git_push_force"),
    ("git -C /d push -f origin main", "n2_git_push_force"),
    (
        'gh api graphql -f query=mutation{deleteRef(input:{refId:"x"}){clientMutationId}}',
        "n2_api_graphql_delete",
    ),
    (
        "gh api graphql -f query=mutation{deleteBranch(input:{}){x}}",
        "n2_api_graphql_delete",
    ),
    ("gh api graphql -F query=@q.graphql -f note=DELETEREF", "n2_api_graphql_delete"),
    ("git branch -d x", "n2_git_branch_delete"),
    ("git branch -D x", "n2_git_branch_delete"),
    ("git branch --delete x", "n2_git_branch_delete"),
    ("git -C /some/dir branch -D x", "n2_git_branch_delete"),
    ("/usr/bin/git branch -D x", "n2_git_branch_delete"),
    ("gh pr merge 1 --delete-branch", "n2_pr_merge_delete_branch"),
    ("gh pr merge 1 --repo o/r --squash -d", "n2_pr_merge_delete_branch"),
    ("gh api -X DELETE repos/o/r/git/refs/heads/x", "n2_api_delete"),
    ("gh api -X DELETE repos/o/r/issues/1/labels/bug", "n2_api_delete"),
    ("gh api -X DELETE repos/o/r/issues/comments/9", "n2_api_delete"),
    ("gh api --method DELETE repos/o/r/issues/comments/9", "n2_api_delete"),
    ("gh api --method=delete repos/o/r/issues/comments/9", "n2_api_delete"),
    ("gh api -XDELETE repos/o/r/issues/comments/9", "n2_api_delete"),
    ("gh api repos/o/r/issues/comments/9 -X DELETE", "n2_api_delete"),
    ("gh api -X DELETE /repos/o/r/issues/1/labels/hold:plan", "n2_api_delete"),
    ("gh api -X DELETE repos/o/r/issues/x/labels/hold:plan", "n2_api_delete"),
    ("gh api -X DELETE repos/o/r/issues/1/labels/hold:plan/more", "n2_api_delete"),
    ("gh api -X DELETE repos/o/r/issues/1/labels/hold:backlog", "n2_api_delete"),
    ("gh issue delete 1 --repo o/r", "n2_data_delete"),
    ("gh repo delete o/r --yes", "n2_data_delete"),
    ("orca worktree rm", "n2_worktree_rm"),
    ("orca worktree rm --worktree id:abc", "n2_worktree_rm"),
    ("orca --json worktree rm", "n2_worktree_rm"),
    ("orca --environment srv worktree rm", "n2_worktree_rm"),
    (
        "orca --pairing-code orca://pair?x=1 orchestration reset",
        "n2_orchestration_reset",
    ),
    ("orca orchestration --json worker-stop --dispatch d", "n7_worker_stop"),
    ("git -c user.name=x -C /d branch -D b", "n2_git_branch_delete"),
    ("git --no-pager --git-dir=/x branch -D b", "n2_git_branch_delete"),
    ("orca orchestration reset", "n2_orchestration_reset"),
    ("ccsession --rm x", "n2_ccsession_rm"),
    ("ccsession orchestrator-x-1 --rm=x", "n2_ccsession_rm"),
    # N3
    ("gh auth login", "n3_gh_auth"),
    ("gh auth logout", "n3_gh_auth"),
    ("gh auth refresh", "n3_gh_auth"),
    ("gh auth token", "n3_gh_auth"),
    ("coder secret create aienv", "n3_coder_secret"),
    ("gh secret set X --repo o/r", "n3_gh_secret"),
    ("cat /home/u/.env", "n3_credential_file"),
    ("tee /home/u/.aienv.local", "n3_credential_file"),
    ("cp x /home/u/.aienv", "n3_credential_file"),
    ("diff /a --file=/home/u/.env", "n3_credential_file"),
    # N4
    ("gh api -X POST repos/o/r/hooks", "n4_api_secret_write"),
    ("gh api -X PUT repos/o/r/actions/secrets/X", "n4_api_secret_write"),
    ("gh api -X POST repos/o/r/keys", "n4_api_secret_write"),
    ("gh api repos/o/r/keys -f title=t", "n4_api_secret_write"),
    ("gh api -X POST app/installations/1/access_tokens", "n4_api_secret_write"),
    ("gh api user/keys --method=POST", "n4_api_secret_write"),
    ("gh api https://api.github.com/repos/o/r/hooks -X PATCH", "n4_api_secret_write"),
    # N5
    ("coder stop ws", "n5_coder_lifecycle"),
    ("coder start ws", "n5_coder_lifecycle"),
    ("coder restart ws", "n5_coder_lifecycle"),
    ("coder update ws", "n5_coder_lifecycle"),
    ("coder delete ws", "n5_coder_lifecycle"),
    ("systemctl restart x", "n5_host_lifecycle"),
    ("shutdown now", "n5_host_lifecycle"),
    ("reboot", "n5_host_lifecycle"),
    ("orca automations create", "n5_automations_write"),
    ("orca automations edit", "n5_automations_write"),
    ("orca automations remove", "n5_automations_write"),
    ("orca automations run", "n5_automations_write"),
    ("orca project add --path /x", "n5_project_other"),
    ("orca project remove x", "n5_project_other"),
    # N7
    ("orca orchestration worker-stop --dispatch d", "n7_worker_stop"),
    ("orca orchestration worker-abandon --dispatch d", "n7_worker_stop"),
]

# The N6 patterns: refused without an accepted answer reference, allowed with one.
GATED = [
    ("git tag v1", "n6_git_tag"),
    ("git tag -a v1 -m msg", "n6_git_tag"),
    ("git tag -d v1", "n6_git_tag"),
    ("git push origin v1", "n6_git_push_tag"),
    ("git push origin refs/tags/v1", "n6_git_push_tag"),
    ("git push origin v1.2.3-rc1", "n6_git_push_tag"),
    ("git push origin HEAD:v2", "n6_git_push_tag"),
    ("git push origin tag v1", "n6_git_push_tag"),
    ("git push --tags", "n6_git_push_tag"),
    ("git push origin --follow-tags", "n6_git_push_tag"),
    ("gh release create v1", "n6_release"),
    ("gh release edit v1", "n6_release"),
    ("gh release delete v1", "n6_release"),
    # the API forms of tagging and releasing (finding F31 of issue 675)
    ("gh api -X POST repos/o/r/releases -f tag_name=v1", "n6_api_release"),
    ("gh api repos/o/r/releases -f tag_name=v1", "n6_api_release"),
    ("gh api -X PATCH repos/o/r/releases/1 -f draft=false", "n6_api_release"),
    ("gh api -X POST repos/o/r/releases/1/assets", "n6_api_release"),
    ("gh api -X POST repos/o/r/git/tags -f tag=v1", "n6_api_release"),
    (
        "gh api -X POST repos/o/r/git/refs -f ref=refs/tags/v1 -f sha=abc1234",
        "n6_api_release",
    ),
    ("gh api -X PATCH repos/o/r/git/refs/tags/v1 -f sha=abc1234", "n6_api_release"),
    ("uv publish", "n6_publish"),
    ("twine upload dist/x.whl", "n6_publish"),
    ("npm publish", "n6_publish"),
]

# N7 with control bytes in the text, and the interrupt (allowed for `escalate` only).
CONTROL_TEXTS = [ESC, ETX, f"a{ESC}b", "\\x1b", "\\x03", "\\u001b", "\\033", "\\X1B"]

PASSING = [
    # the poll's one DELETE and the read-only commands the design names
    "gh api -X DELETE repos/o/r/issues/1/labels/hold:plan",
    "gh api --method DELETE repos/o/r/issues/12/labels/hold:plan",
    "orca automations list",
    "orca automations show x",
    "orca automations runs x",
    # deleting ordinary files stays allowed (ruling 25)
    "rm .orchestrator/wakes/done/x.json",
    "git -C /work/tree rm file.txt",
    "git rm file.txt",
    # what each wave uses
    "gh issue view 1 --repo o/r --json state,assignees,comments",
    "gh issue view 1 --repo o/r --json number,title,body,state,labels,comments",
    "gh pr merge 1 --repo o/r --squash --match-head-commit abc1234",
    "gh pr view 1 --repo o/r --json state",
    "gh api repos/o/r/issues/1",
    "gh api -X GET repos/o/r/issues -f state=open",
    "gh api repos/o/r/hooks",
    "gh api repos/o/r/releases",
    "gh api repos/o/r/git/refs/tags/v1",
    "gh api -X POST repos/o/r/git/refs -f ref=refs/heads/x -f sha=abc1234",
    "gh api -X GET repos/o/r/keys -f x=y",
    "gh api -X POST repos/o/r/issues/1/labels -f labels[]=hold:plan",
    "gh api graphql -f query=query{viewer{login}}",
    "gh auth status",
    "gh release view v1",
    "gh release list",
    "git status --porcelain --untracked-files=no",
    "git fetch origin",
    "git -C /checkout remote get-url origin",
    "git switch -c issue-5-r2 origin/main",
    "git branch issue-5-r2",
    "git branch --list",
    "git branch -vv",
    "git push origin issue-5-fix",
    "git push -u origin HEAD",
    "git tag",
    "git tag --list",
    "git tag -l v*",
    "git tag --contains abc1234",
    "orca skills get orchestration",
    "orca orchestration run-create --objective x --json",
    "orca orchestration worker-list --run r --json",
    "orca orchestration worker-start --task t --worktree path:/w --agent claude",
    "orca orchestration worker-read --dispatch d --source transcript --limit 200",
    "orca orchestration send --to run:r --type status --subject worker-stop",
    "orca terminal list --worktree path:/w --json",
    "orca terminal send --terminal t --text yes --enter",
    "orca terminal send --terminal t --text hello --wait-submit 5",
    "orca terminal close --terminal t",
    "orca worktree ps",
    "orca worktree show --worktree issue:1 --json",
    "orca project setup-clone --project github:o/r --host local --url u --destination /c",
    "orca reference find u --json",
    "ccsession --list",
    "uv run pytest -q",
    "uv pip install x",
    "coder list",
    "cat /home/u/.env.example",
]


@pytest.mark.parametrize(("line", "reason"), REFUSED, ids=[a for a, _ in REFUSED])
def test_refuse_a_pattern_of_n2_to_n7(line: str, reason: str) -> None:
    assert refuse(argv(line)) == reason
    # an accepted answer and the interrupt caller open no way through these
    assert refuse(argv(line), answer_ref=ANSWER_REF, caller="escalate") == reason


@pytest.mark.parametrize(("line", "reason"), GATED, ids=[a for a, _ in GATED])
def test_n6_passes_only_with_an_accepted_answer_reference(
    line: str, reason: str
) -> None:
    assert refuse(argv(line)) == reason
    assert refuse(argv(line), answer_ref=None) == reason
    assert refuse(argv(line), answer_ref="") == reason
    assert refuse(argv(line), answer_ref="two words") == reason
    assert refuse(argv(line), answer_ref="x\ny") == reason
    assert (
        refuse(argv(line), caller="escalate") == reason
    )  # the caller does not open N6
    assert refuse(argv(line), answer_ref=ANSWER_REF) is None


@pytest.mark.parametrize("text", CONTROL_TEXTS, ids=repr)
def test_n7_refuses_escape_and_ctrl_c_sent_as_bytes(text: str) -> None:
    for form in (["--text", text], [f"--text={text}"]):
        call = ["orca", "terminal", "send", "--terminal", "t", *form, "--enter"]
        assert refuse(call) == "n7_control_bytes"
        assert (
            refuse(call, answer_ref=ANSWER_REF, caller="escalate") == "n7_control_bytes"
        )


def test_n7_interrupt_passes_only_for_the_escalate_caller() -> None:
    call = argv("orca terminal send --terminal t --interrupt")
    assert refuse(call) == "n7_interrupt"
    assert refuse(call, caller="report-entry") == "n7_interrupt"
    assert refuse(call, answer_ref=ANSWER_REF) == "n7_interrupt"
    assert refuse(call, caller="escalate") is None


@pytest.mark.parametrize("line", PASSING)
def test_the_ordinary_commands_of_the_waves_pass(line: str) -> None:
    assert refuse(argv(line)) is None


@pytest.mark.parametrize(
    "bad", [[], (), "git push --delete x", ["git", 5], ["git", None], None], ids=repr
)
def test_an_argv_that_is_not_a_list_of_strings_is_refused(bad: object) -> None:
    assert refuse(bad) == ARGV_INVALID  # type: ignore[arg-type]


def test_a_reason_is_a_fixed_code_and_never_holds_an_argument_value() -> None:
    codes = {r.code for r in RULES} | {ARGV_INVALID}
    for line, _ in REFUSED + GATED:
        reason = refuse(argv(line))
        assert reason in codes
        assert re.fullmatch(r"[a-z0-9_]+", reason)
    secret = "SECRET-VALUE-123"
    assert refuse(["gh", "secret", "set", "X", "--body", secret]) == "n3_gh_secret"
    assert secret not in (refuse(["gh", "secret", "set", "X", "--body", secret]) or "")


# --- the table and the data -------------------------------------------------------------


def test_every_rule_belongs_to_a_row_and_every_row_has_a_pattern() -> None:
    assert {r.row for r in RULES} == set(RULE_ROWS)
    assert len({r.code for r in RULES}) == len(RULES)
    for rule in RULES:
        assert rule.code.startswith(rule.row.lower() + "_")
        assert rule.gate in (None, "answer_ref", "escalate")
        assert rule.row == "N6" or rule.gate in (None, "escalate")
    assert {r.row for r in RULES if r.gate == "answer_ref"} == {"N6"}
    assert {r.row for r in RULES if r.gate == "escalate"} == {"N7"}


def test_each_pattern_has_a_failing_case_in_this_file() -> None:
    covered = {reason for _, reason in REFUSED + GATED}
    covered |= {"n7_control_bytes", "n7_interrupt"}
    assert covered == {r.code for r in RULES}


def _spec_rows() -> list[str]:
    text = SPEC.read_text(encoding="utf-8")
    start = text.index("**May never (requirement).**")
    end = text.index("**The refusal, in code.**")
    return re.findall(r"^\| (N[0-9]+) \|", text[start:end], re.M)


@pytest.mark.skipif(not SPEC.exists(), reason="the design is not on this branch yet")
def test_the_n_rows_of_the_design_and_the_data_agree_in_both_directions() -> None:
    spec_rows = set(_spec_rows())
    assert spec_rows == {"N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"}
    # N1 (the permanent "always allow") and N8 (grants) are covered by tests of the
    # typing and grant checks, not by an argv pattern
    with_patterns = spec_rows - {"N1", "N8"}
    assert with_patterns == {
        r.row for r in RULES
    }  # every row has a pattern, and no pattern has no row


def test_the_rows_with_patterns_are_n2_to_n7() -> None:
    assert RULE_ROWS == ("N2", "N3", "N4", "N5", "N6", "N7")


# --- the runner every verb uses ------------------------------------------------------------


class FakeInner:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        self.calls.append(list(argv))
        return CommandResult(tuple(argv), 0, "ok", "", False, None, 0.0)


def test_a_guarded_runner_does_not_run_a_refused_argv() -> None:
    inner = FakeInner()
    runner = GuardedRunner(inner, caller="merge-gate")
    with pytest.raises(Refused) as caught:
        runner.run(["gh", "pr", "merge", "1", "--delete-branch", "--repo", "o/r"], 5.0)
    assert caught.value.reason == "n2_pr_merge_delete_branch"
    assert (
        str(caught.value) == "n2_pr_merge_delete_branch"
    )  # no argument value in the text
    assert inner.calls == []


def test_a_guarded_runner_runs_an_allowed_argv_and_passes_the_answer_and_caller() -> (
    None
):
    inner = FakeInner()
    runner = GuardedRunner(inner, caller="escalate", answer_ref=ANSWER_REF)
    ok = runner.run(["gh", "issue", "view", "1"], 5.0, cwd="/w")
    assert ok.stdout == "ok"
    runner.run(["git", "tag", "v1"], 5.0)  # the answer reference opens N6
    runner.run(["orca", "terminal", "send", "--terminal", "t", "--interrupt"], 5.0)
    assert len(inner.calls) == 3
    with pytest.raises(Refused):
        GuardedRunner(inner).run(["git", "tag", "v1"], 5.0)


def test_a_verb_exits_2_with_the_reason_and_never_the_argument_values() -> None:
    inner = FakeInner()

    @click.command()
    def verb() -> None:
        runner = GuardedRunner(inner, caller="merge-gate")

        def action() -> dict:
            runner.run(
                ["gh", "secret", "set", "TOKEN", "--body", "SECRET-VALUE-123"], 5.0
            )
            return {}

        common.run(action)

    result = CliRunner().invoke(verb)
    assert result.exit_code == limits.EXIT_REFUSED == 2
    assert json.loads(result.output) == {"ok": False, "reason": "n3_gh_secret"}
    assert "SECRET-VALUE-123" not in result.output and "TOKEN" not in result.output
    assert inner.calls == []


def test_every_argv_of_the_polls_label_writer_passes_the_refusal() -> None:
    """``LabelWriter(runner, guard=limits.refuse)`` must never block the poll's own writes."""
    for call in (
        github.argv_label_get("o/r"),
        github.argv_label_create("o/r"),
        github.argv_label_add("o/r", 12),
        github.argv_label_remove("o/r", 12),
    ):
        assert refuse(call) is None, call


def test_the_poll_guard_form_is_the_function_itself() -> None:
    """``LabelWriter(runner, guard=limits.refuse)`` calls ``guard(list(argv))``."""
    assert (
        limits.refuse(argv("gh api -X DELETE repos/o/r/issues/1/labels/hold:plan"))
        is None
    )
    assert (
        limits.refuse(argv("gh api -X DELETE repos/o/r/issues/1/labels/bug"))
        is not None
    )
    assert limits.EXIT_REFUSED == 2
