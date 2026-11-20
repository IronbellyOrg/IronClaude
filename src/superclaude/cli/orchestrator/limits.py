"""The refusal of the orchestrator as a control plane (design 5.9, rows N2 to N7).

One function, :func:`refuse`, holds the patterns of the "may never" table as
data (``RULES``). Every ``gh``, ``git`` and ``orca`` call that a
``superclaude orchestrator`` verb makes goes through it, by way of
:class:`GuardedRunner`, and the poll's label writer passes its one ``DELETE``
through it too (``LabelWriter(runner, guard=refuse)``). A refused argv is not
run: the verb exits 2 with the reason and never prints the argument values.

``refuse(argv, answer_ref=None, caller=None)`` returns a reason code such as
``n2_git_branch_delete`` to refuse, or ``None`` to allow:

* the N6 patterns (tags, releases, package uploads) pass only with an
  ``answer_ref``, the reference of an answer that ``answer-check`` accepted. This
  module checks only that the reference is well formed; ``answer-check`` decides
  whether it is accepted;
* the ``--interrupt`` pattern of N7 passes only when ``caller`` is
  ``escalate`` (``superclaude orchestrator escalate --interrupt``);
* every other pattern refuses with no way through.

Stated limits (spec 5.9, "Stated limits"): the refusal sees only the argv lists
that the verbs run. It matches the leading words of a command, after any leading
option, so it stops a confused agent and not a determined one. A command the
model types with its own shell is bounded by the skill's "Will Not Do" and by
the text scan of the skill, not by this module. Two reading rules are chosen to
fail closed: a ``git push`` ref that reads like a release tag (``v1``,
``1.2.3``, ``refs/tags/...``) is a tag push, and a ``gh api`` call with a field
and no method is a write.

Scope of the list (findings F28 and F65 of issue 675): this is a denylist, so it
is the only closed list here. Everything it does not name passes: ``git fetch``,
``git switch -c``, ``git status``, the plan call, ``rm`` and ``git rm`` of any
ordinary file. Deleting ordinary files is allowed by ruling 25 and there is no
``rm`` pattern and no list of folders; the rows of 5.9 that name a location
describe what the orchestrator does, not what this function checks.

Releases (owner ruling on question Q2 of the B1 report): ``N2`` says the
orchestrator never deletes a release and ``N6`` allows ``gh release delete`` with
a recorded OK. Both stay as built and the stricter side wins where the forms
differ: the command ``gh release delete`` is gated by ``N6`` (it passes with an
accepted ``answer_ref``), while the API form ``gh api -X DELETE repos/<R>/releases/<id>``
is refused by ``N2`` with no way through.

Shared branch history is a hard bar (``N2``): a force push (``--force``,
``--force-with-lease``, ``-f``, a refspec that starts with ``+``, ``--mirror``), a
branch deletion by ``git push --delete`` or a ``:branch`` refspec, and a GraphQL
call whose text holds ``deleteRef`` or ``deleteBranch`` are refused. A GraphQL
document passed from a file (``--input``) cannot be read here: that is a stated
limit.
"""

from __future__ import annotations

import os
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Final
from urllib.parse import urlsplit

from superclaude.cli.issue_watch.predicates import (
    HOLD_LABEL,
    valid_issue_number,
    valid_repo,
)
from superclaude.cli.issue_watch.runner import CommandResult, Runner

EXIT_REFUSED: Final = 2
"""The exit code of a verb that refused an argv."""

ESCALATE_CALLER: Final = "escalate"
"""The one caller that may run ``orca terminal send --interrupt`` (N7)."""

RULE_ROWS: Final = ("N2", "N3", "N4", "N5", "N6", "N7")
"""The rows of the table of 5.9 that have patterns (N1 and N8 are covered elsewhere)."""

ARGV_INVALID: Final = "argv_invalid"
"""Not an N row: the argv is not a non-empty list of strings, so nothing can be checked."""

CREDENTIAL_FILES: Final = frozenset({".env", ".aienv", ".aienv.local"})
SECRET_SEGMENTS: Final = frozenset(
    {"secrets", "keys", "hooks", "installations", "tokens", "access_tokens"}
)
_WRITE_METHODS: Final = frozenset({"POST", "PUT", "PATCH", "DELETE"})

_ANSWER_REF = re.compile(r"[A-Za-z0-9._:#@/=+-]{1,200}")
_HOLD_PATH = re.compile(
    r"repos/(?P<repo>[^/]+/[^/]+)/issues/(?P<n>[0-9]+)/labels/" + re.escape(HOLD_LABEL)
)
_TAG_REF = re.compile(
    r"refs/tags/.+|v?[0-9]+(?:\.[0-9A-Za-z]+)*(?:[-+][0-9A-Za-z.+-]+)?"
)
_CONTROL_BYTES = re.compile(r"[\x1b\x03]|\\(?:x1b|x03|u001b|u0003|033|003)", re.I)

_VALUE_OPTIONS: Final = {
    "git": frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace"}),
    "orca": frozenset({"--pairing-code", "--environment"}),
}
"""Options that take their value as the next token, before the subcommand words."""
_MAX_WORDS: Final = 3
_API_VALUE_LONG = frozenset(
    {
        "--method",
        "--header",
        "--raw-field",
        "--field",
        "--input",
        "--jq",
        "--template",
        "--hostname",
        "--cache",
        "--preview",
    }
)
_API_VALUE_SHORT = frozenset({"-X", "-H", "-f", "-F", "-q", "-t", "-p"})
_API_FIELD_OPTIONS = frozenset({"--raw-field", "--field", "--input", "-f", "-F"})
_TAG_READ_FLAGS = frozenset(
    {
        "-l",
        "--list",
        "--contains",
        "--no-contains",
        "--merged",
        "--no-merged",
        "--points-at",
        "--sort",
        "--format",
        "--column",
        "--color",
    }
)
_TAG_WRITE_LETTERS = frozenset("asufdmF")


# --- reading one argv ----------------------------------------------------------------


def _has_flag(tokens: Sequence[str], *names: str) -> bool:
    """True when a token is one of ``names`` or ``name=value``."""
    return any(t == n or t.startswith(n + "=") for t in tokens for n in names)


def _option_values(tokens: Sequence[str], name: str) -> list[str]:
    """Every value of ``name``: the token after it, or the text after ``name=``."""
    found: list[str] = []
    for i, token in enumerate(tokens):
        if token == name and i + 1 < len(tokens):
            found.append(tokens[i + 1])
        elif token.startswith(name + "="):
            found.append(token[len(name) + 1 :])
    return found


def _short_cluster_has(tokens: Sequence[str], letters: frozenset[str]) -> bool:
    """True when a single-dash token such as ``-fd`` holds one of ``letters``."""
    return any(
        len(t) > 1 and t[0] == "-" and t[1] != "-" and letters & set(t[1:])
        for t in tokens
    )


@dataclass(frozen=True)
class _Gh:
    method: str | None
    fields: bool
    endpoint: str | None

    @property
    def writes(self) -> bool:
        if self.method is not None:
            return self.method in _WRITE_METHODS
        return self.fields  # gh sends POST when a field is given and no method

    @property
    def segments(self) -> list[str]:
        return _endpoint_segments(self.endpoint or "")


def _endpoint_segments(endpoint: str) -> list[str]:
    path = urlsplit(endpoint).path if "://" in endpoint else endpoint.split("?", 1)[0]
    return [s.lower() for s in path.strip("/").split("/") if s]


def _gh_api(tokens: Sequence[str]) -> _Gh:
    """Read the method, the fields and the endpoint of the tokens after ``gh api``."""
    method: str | None = None
    fields = False
    endpoint: str | None = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.startswith("--"):
            name, eq, value = token.partition("=")
            if name in _API_VALUE_LONG:
                if not eq:
                    i += 1
                    value = tokens[i] if i < len(tokens) else ""
                if name == "--method":
                    method = value.upper()
                if name in _API_FIELD_OPTIONS:
                    fields = True
        elif len(token) > 1 and token[0] == "-":
            if token[:2] in _API_VALUE_SHORT:
                value = token[2:].lstrip("=")
                if not value:
                    i += 1
                    value = tokens[i] if i < len(tokens) else ""
                if token[:2] == "-X":
                    method = value.upper()
                if token[:2] in _API_FIELD_OPTIONS:
                    fields = True
        elif endpoint is None:
            endpoint = token
        i += 1
    return _Gh(method, fields, endpoint)


# --- the extra tests of the patterns (named in RULES.extra) --------------------------


def _git_branch_delete(after: Sequence[str]) -> bool:
    return _has_flag(after, "--delete") or _short_cluster_has(after, frozenset("dD"))


def _git_push_delete(after: Sequence[str]) -> bool:
    if _has_flag(after, "--delete") or _short_cluster_has(after, frozenset("d")):
        return True
    refspecs = [t for t in after if not t.startswith("-")][
        1:
    ]  # the first is the remote
    return any(r.startswith(":") for r in refspecs)  # ``git push origin :branch``


def _git_push_force(after: Sequence[str]) -> bool:
    """A push that rewrites a remote branch: force flags, ``--mirror`` or a ``+`` refspec."""
    if _has_flag(
        after, "--force", "--force-with-lease", "--force-if-includes", "--mirror"
    ):
        return True
    if _short_cluster_has(after, frozenset("f")):
        return True
    refspecs = [t for t in after if not t.startswith("-")][1:]
    return any(r.startswith("+") for r in refspecs)


def _api_graphql_delete(after: Sequence[str]) -> bool:
    """A ``gh api graphql`` call whose text deletes a branch or a ref."""
    api = _gh_api(after)
    if api.endpoint != "graphql":
        return False
    text = " ".join(after).lower()
    return "deleteref" in text or "deletebranch" in text


def _is_hold_label_path(endpoint: str | None) -> bool:
    """Exactly ``repos/<R>/issues/<N>/labels/hold:plan``: the poll's one DELETE."""
    match = _HOLD_PATH.fullmatch(endpoint or "")
    return (
        match is not None
        and valid_repo(match["repo"])
        and valid_issue_number(int(match["n"]))
    )


def _api_delete_other(after: Sequence[str]) -> bool:
    api = _gh_api(after)
    return api.method == "DELETE" and not _is_hold_label_path(api.endpoint)


def _api_secret_write(after: Sequence[str]) -> bool:
    api = _gh_api(after)
    return api.writes and bool(SECRET_SEGMENTS.intersection(api.segments))


def _credential_file(after: Sequence[str]) -> bool:
    for token in after:
        value = (
            token.split("=", 1)[1] if token.startswith("-") and "=" in token else token
        )
        if os.path.basename(value.rstrip("/")) in CREDENTIAL_FILES:
            return True
    return False


def _project_other(after: Sequence[str]) -> bool:
    verb = next((t for t in after if not t.startswith("-")), None)
    return verb is not None and verb != "setup-clone"


def _git_tag_write(after: Sequence[str]) -> bool:
    if _short_cluster_has(after, _TAG_WRITE_LETTERS):
        return True
    if _has_flag(
        after, "--annotate", "--sign", "--force", "--delete", "--message", "--file"
    ):
        return True
    reading = _has_flag(after, *_TAG_READ_FLAGS) or "-l" in after
    return not reading and any(not t.startswith("-") for t in after)


def _is_tag_ref(ref: str) -> bool:
    return _TAG_REF.fullmatch(ref.lstrip("+")) is not None


def _git_push_tag(after: Sequence[str]) -> bool:
    if _has_flag(after, "--tags", "--follow-tags", "--tag"):
        return True
    positional = [t for t in after if not t.startswith("-")]
    if "tag" in positional[1:]:  # ``git push origin tag v1``
        return True
    return any(
        _is_tag_ref(part) for r in positional[1:] for part in r.split(":") if part
    )


def _api_release_write(after: Sequence[str]) -> bool:
    """A write through the API that tags or releases (finding F31 of issue 675).

    ``repos/<R>/releases...`` (a release or an asset), ``repos/<R>/git/tags`` and
    ``repos/<R>/git/refs/tags/...``, or a ``ref=refs/tags/...`` field on any write.
    """
    api = _gh_api(after)
    if not api.writes:
        return False
    segments = api.segments
    return (
        "releases" in segments
        or ("git" in segments and "tags" in segments)
        or any("ref=refs/tags/" in token for token in after)
    )


def _send_control_bytes(after: Sequence[str]) -> bool:
    return any(_CONTROL_BYTES.search(v) for v in _option_values(after, "--text"))


def _send_interrupt(after: Sequence[str]) -> bool:
    return _has_flag(after, "--interrupt")


_EXTRA: Final[dict[str, Callable[[Sequence[str]], bool]]] = {
    "git_branch_delete": _git_branch_delete,
    "git_push_delete": _git_push_delete,
    "git_push_force": _git_push_force,
    "api_graphql_delete": _api_graphql_delete,
    "api_delete_other": _api_delete_other,
    "api_secret_write": _api_secret_write,
    "credential_file": _credential_file,
    "project_other": _project_other,
    "git_tag_write": _git_tag_write,
    "git_push_tag": _git_push_tag,
    "api_release_write": _api_release_write,
    "send_control_bytes": _send_control_bytes,
    "send_interrupt": _send_interrupt,
}


# --- the patterns, as data ------------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    """One refusal pattern.

    ``progs`` are program base names (empty: any program). ``words`` are the
    alternatives for the leading words after the program (empty: none needed).
    ``flags`` refuse when any is present. ``extra`` names a further test in
    ``_EXTRA`` that must hold. ``gate`` is ``None`` (no way through),
    ``"answer_ref"`` (passes with an accepted answer) or ``"escalate"`` (passes
    for the caller ``escalate``).
    """

    row: str
    code: str
    progs: tuple[str, ...] = ()
    words: tuple[tuple[str, ...], ...] = ()
    flags: tuple[str, ...] = ()
    extra: str | None = None
    gate: str | None = None


RULES: Final[tuple[Rule, ...]] = (
    # N2: deletes what the rulings reserve to Clay
    Rule(
        "N2", "n2_git_branch_delete", ("git",), (("branch",),), (), "git_branch_delete"
    ),
    Rule("N2", "n2_git_push_delete", ("git",), (("push",),), (), "git_push_delete"),
    Rule("N2", "n2_git_push_force", ("git",), (("push",),), (), "git_push_force"),
    Rule("N2", "n2_api_graphql_delete", ("gh",), (("api",),), (), "api_graphql_delete"),
    Rule(
        "N2",
        "n2_pr_merge_delete_branch",
        ("gh",),
        (("pr", "merge"),),
        ("--delete-branch", "-d"),
    ),
    Rule("N2", "n2_api_delete", ("gh",), (("api",),), (), "api_delete_other"),
    Rule("N2", "n2_data_delete", ("gh",), (("issue", "delete"), ("repo", "delete"))),
    Rule(
        "N2",
        "n2_worktree_rm",
        ("orca",),
        (("worktree", "rm"), ("worktree", "remove")),
    ),
    Rule("N2", "n2_orchestration_reset", ("orca",), (("orchestration", "reset"),)),
    Rule("N2", "n2_ccsession_rm", ("ccsession",), (), ("--rm",)),
    # N3: changes credentials
    Rule(
        "N3",
        "n3_gh_auth",
        ("gh",),
        tuple(
            ("auth", v)
            for v in ("login", "logout", "refresh", "switch", "token", "setup-git")
        ),
    ),
    Rule("N3", "n3_coder_secret", ("coder",), (("secret",), ("secrets",))),
    Rule("N3", "n3_gh_secret", ("gh",), (("secret",),)),
    Rule("N3", "n3_credential_file", (), (), (), "credential_file"),
    # N4: mints or rotates secrets
    Rule("N4", "n4_api_secret_write", ("gh",), (("api",),), (), "api_secret_write"),
    # N5: controls machine or VM lifecycle
    Rule(
        "N5",
        "n5_coder_lifecycle",
        ("coder",),
        tuple(
            (v,)
            for v in ("start", "stop", "restart", "update", "delete", "create", "rm")
        ),
    ),
    Rule(
        "N5",
        "n5_host_lifecycle",
        ("shutdown", "reboot", "poweroff", "halt", "systemctl"),
    ),
    Rule(
        "N5",
        "n5_automations_write",
        ("orca",),
        tuple(("automations", v) for v in ("create", "edit", "remove", "run")),
    ),
    Rule("N5", "n5_project_other", ("orca",), (("project",),), (), "project_other"),
    # N6: tags or publishes a release without a recorded human OK
    Rule("N6", "n6_git_tag", ("git",), (("tag",),), (), "git_tag_write", "answer_ref"),
    Rule(
        "N6",
        "n6_git_push_tag",
        ("git",),
        (("push",),),
        (),
        "git_push_tag",
        "answer_ref",
    ),
    Rule(
        "N6",
        "n6_release",
        ("gh",),
        tuple(("release", v) for v in ("create", "edit", "delete")),
        (),
        None,
        "answer_ref",
    ),
    Rule(
        "N6",
        "n6_api_release",
        ("gh",),
        (("api",),),
        (),
        "api_release_write",
        "answer_ref",
    ),
    Rule(
        "N6",
        "n6_publish",
        ("uv", "twine", "npm", "pnpm", "yarn", "cargo", "poetry"),
        (("publish",), ("upload",)),
        (),
        None,
        "answer_ref",
    ),
    # N7: stops a worker, except for one interrupt
    Rule(
        "N7",
        "n7_worker_stop",
        ("orca",),
        (("orchestration", "worker-stop"), ("orchestration", "worker-abandon")),
    ),
    Rule(
        "N7",
        "n7_control_bytes",
        ("orca",),
        (("terminal", "send"),),
        (),
        "send_control_bytes",
    ),
    Rule(
        "N7",
        "n7_interrupt",
        ("orca",),
        (("terminal", "send"),),
        (),
        "send_interrupt",
        "escalate",
    ),
)


# --- the function ---------------------------------------------------------------------


def _leading_words(prog: str, tokens: Sequence[str]) -> tuple[list[str], list[int]]:
    """The first words of the command and the token index just after each of them.

    An option between the words is skipped (with its value for the options of
    ``_VALUE_OPTIONS``), so ``git -C dir tag v1`` and ``orca --json worktree rm``
    read as ``tag v1`` and ``worktree rm``.
    """
    words: list[str] = []
    ends: list[int] = []
    value_options = _VALUE_OPTIONS.get(prog, frozenset())
    i = 0
    while i < len(tokens) and len(words) < _MAX_WORDS:
        if tokens[i].startswith("-"):
            i += 2 if tokens[i] in value_options else 1
        else:
            words.append(tokens[i])
            i += 1
            ends.append(i)
    return words, ends


def _matches(rule: Rule, prog: str, tokens: Sequence[str]) -> bool:
    if rule.progs and prog not in rule.progs:
        return False
    words, ends = _leading_words(prog, tokens)
    if rule.words:
        for alt in rule.words:
            if tuple(words[: len(alt)]) == alt:
                after = tokens[ends[len(alt) - 1] :]
                break
        else:
            return False
    else:
        after = tokens
    if rule.flags and not _has_flag(after, *rule.flags):
        return False
    return rule.extra is None or _EXTRA[rule.extra](after)


def _valid_answer_ref(answer_ref: object) -> bool:
    return isinstance(answer_ref, str) and _ANSWER_REF.fullmatch(answer_ref) is not None


def refuse(
    argv: Sequence[str],
    answer_ref: str | None = None,
    caller: str | None = None,
) -> str | None:
    """Return the reason code that refuses ``argv``, or ``None`` to allow it.

    The reason is a fixed code of ``RULES`` and never holds an argument value.
    ``answer_ref`` is the reference of an answer that ``answer-check`` accepted (it
    lets the N6 patterns through); ``caller`` is the name of the verb making the
    call (``escalate`` lets the interrupt through).
    """
    if (
        not isinstance(argv, (list, tuple))
        or not argv
        or not all(isinstance(a, str) for a in argv)
    ):
        return ARGV_INVALID
    prog = os.path.basename(argv[0])
    tokens = list(argv[1:])
    for rule in RULES:
        if not _matches(rule, prog, tokens):
            continue
        if rule.gate == "answer_ref" and _valid_answer_ref(answer_ref):
            continue
        if rule.gate == ESCALATE_CALLER and caller == ESCALATE_CALLER:
            continue
        return rule.code
    return None


# --- the runner every verb uses -------------------------------------------------------


class Refused(Exception):
    """A call was refused by :func:`refuse`; ``reason`` is the code, never the argv."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class GuardedRunner:
    """A ``Runner`` that checks each argv with :func:`refuse` before it runs it.

    A refused call raises :class:`Refused` and the inner runner is never called.
    The verb turns the exception into exit ``EXIT_REFUSED`` and a message made of
    the reason alone.
    """

    def __init__(
        self,
        inner: Runner,
        *,
        caller: str | None = None,
        answer_ref: str | None = None,
    ) -> None:
        self._inner = inner
        self._caller = caller
        self._answer_ref = answer_ref

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        """Run ``argv`` through the inner runner unless a pattern refuses it."""
        reason = refuse(argv, self._answer_ref, self._caller)
        if reason is not None:
            raise Refused(reason)
        return self._inner.run(argv, timeout, cwd=cwd)
