"""Static checks for the Orca worker contract (~/.claude/WORKER-CONTRACT.md), Phase P0.

The contract file is read through the module-level CONTRACT_PATH and the command
files through COMMANDS_DIR, so the negative tests can point both at a tmp_path copy.
Each rule is pinned by phrases that carry its meaning, not only its label. The
phrases are copied here as data; the tests never read the plan's artifacts.
CI-safe, no network.
"""

import re
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
CONTRACT_PATH = _REPO / "src" / "superclaude" / "core" / "WORKER-CONTRACT.md"
COMMANDS_DIR = _REPO / "src" / "superclaude" / "commands"

_THIS = sys.modules[__name__]

# rule -> (identifier that must share a line with the first phrase, or None; phrases)
RULE_PHRASES = {
    # Terms
    "worker-run": (
        None,
        [
            "a session that received an Orca preamble carrying a Task ID and a Dispatch ID"
        ],
    ),
    "unattended-mode": (
        None,
        [
            "The mode is selected only by the flag (decision D1)",
            "No command detects Orca, its preamble or its environment",
        ],
    ),
    "flag-parse-rule": (
        None,
        ["counts only as a standalone argument token outside any quoted argument"],
    ),
    "person-mode-refusal": (
        None,
        ["every command refuses the flags that exist to involve a person"],
    ),
    "report-directory": (
        None,
        ["Passing neither, or both, is refused before any work"],
    ),
    "brief-guard-scope": (
        None,
        [
            "it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs"
        ],
    ),
    "brief-guard-case-1": (
        None,
        [
            "(case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended`",
            "guard refused: brief lacks --unattended",
        ],
    ),
    "brief-guard-case-2": (
        None,
        [
            "(case 2) no existing copy has the section and the line has the flag",
            "guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)",
        ],
    ),
    "brief-guard-copies-disagree": (
        None,
        [
            "the copies disagree",
            "guard refused: command copies disagree (stale copy): <paths>",
        ],
    ),
    "brief-guard-case-3": (
        None,
        [
            "(case 3) the command is on the never-as-worker list; the body still starts `guard refused:`"
        ],
    ),
    "brief-guard-prefix": (None, ["a body starting `guard refused:`"]),
    "never-as-worker": (
        "**Never-as-worker list**",
        [
            "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, "
            "plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers"
        ],
    ),
    "nested-propagation": (
        None,
        [
            "passes `--unattended` when the invoked command accepts it at this phase",
            "`<caller report-dir>/nested/<command>-<n>/`",
        ],
    ),
    # Command-side requirements
    "WC-2": ("WC-2", ["No person-blocking step in unattended mode"]),
    "WC-4": (
        "WC-4",
        [
            "One report file, known before dispatch, written on every outcome",
            '`worker_contract_version` (`"1"`), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path`',
            "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed",
        ],
    ),
    "WC-4-mapping": (
        None,
        [
            "`success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, `stopped-precondition` → `failed`"
        ],
    ),
    "WC-4-missing-directory-error": (
        None,
        [
            "unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag"
        ],
    ),
    "WC-8": ("WC-8", ["No Orca fan-out from inside a command"]),
    "WC-9": ("WC-9", ["No outward action from a worker; local commits only by grant"]),
    "WC-10": (
        "WC-10",
        ["at the cadence its preamble sets", "split into waits of at most 4 minutes"],
    ),
    "WC-11": ("WC-11", ["Two workers in one worktree must never write the same file"]),
    # Worker-session duties
    "WC-3": (
        "WC-3",
        [
            "Questions go to the coordinator, not to a local prompt",
            "The worker asks at most once per Task",
        ],
    ),
    "WC-5": (
        "WC-5",
        [
            "`--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists"
        ],
    ),
    "WC-5-P0-override": (
        "WC-5",
        [
            "a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task"
        ],
    ),
    "WC-7": ("WC-7", ["Run at the top level, never inside a subagent"]),
    "WC-12": (
        "WC-12",
        ["Coordinator follow-ups are pulled, not pushed", "at natural checkpoints"],
    ),
    "WC-13": ("WC-13", ["No Orca fan-out from the worker session"]),
    "heartbeats": (
        None,
        [
            "The worker session sends heartbeats at the cadence its preamble sets",
            "the dispatch preamble is the authority for the Orca verb syntax and for the heartbeat cadence",
        ],
    ),
    # Coordinator rules
    "WC-6": (
        "WC-6",
        [
            "WC-6. Every retry is a new Task",
            "the coordinator never uses `worker-start --retry-of`",
            "is never re-created after three failed starts",
            "A crashed or stalled attempt is settled by the coordinator",
        ],
    ),
    "brief-contents": (
        None,
        [
            "The contract only works if the brief carries what the command would otherwise ask a person",
            "at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5)",
        ],
    ),
    "brief-layout": (None, ["so the Task text never starts with `/sc:`"]),
    "worktrees": (
        None,
        [
            "Every worktree is created by Orca at Orca's default location",
            "a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>` when WC-11 requires one",
            "The coordinator keeps a placement map",
            "the coordinator merges the child branch into the feature branch, then removes the child",
            "It never removes a worktree or branch that holds unmerged commits",
        ],
    ),
    "child-setup": (
        "`--setup skip`",
        [
            "where `git remote get-url origin` run in the coordinator's feature worktree prints exactly `https://github.com/IronbellyOrg/IronClaude` or `git@github.com:IronbellyOrg/IronClaude`",
            "only when the user's instruction, in the coordinator's own conversation, names that step",
        ],
    ),
    "git-github-ownership": (
        None,
        [
            "Every such action targets `IronbellyOrg/IronClaude`",
            "PRs go only through `/sc:pr-submit --monitor 3`",
            "Before any push that would publish worker commits the person has not seen",
            "stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run",
        ],
    ),
    "read-before-depend": (
        None,
        [
            "Reading a result before anything depends on it",
            "a brief-guard refusal; nothing ran",
        ],
    ),
    "dependents-after-settle": (
        None,
        ["Every dependent Task is created only after all its inputs have settled"],
    ),
    "implement-stop": (
        None,
        [
            "*Freeze.* A plan is frozen when",
            "*Lifting the freeze.* The freeze lifts only when",
            "dispatches only if all of the following hold",
            "*Placement.* The resume Task starts in the halted worktree by selector",
        ],
    ),
    "fan-in-max": (None, ["maximum of 10 inputs"]),
    "fan-in-min": (None, ["at least 2 inputs are admitted"]),
    "brief-template": (
        None,
        [
            "## 5. Coordinator brief template",
            '`--report-dir` is marked "from P1": no command accepts it at P0',
            "P0 only: Report file: <the command's report file under AC-0.4>.",
        ],
    ),
}

GUARD_LINE = (
    "Guard: before running anything, check every Command: line below under the brief guard in "
    "~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed "
    'with a body starting "guard refused:".'
)

NEVER_AS_WORKER = (
    "/sc:agent",
    "/sc:git",
    "/sc:help",
    "/sc:pm",
    "/sc:spawn",
    "/sc:swarm-wizard",
    "/sc:pr-submit",
)

# Commands with an `## Unattended mode` section after P0 (./source.md section 6
# table: none). Later phases extend this set.
UNATTENDED_COMMANDS: frozenset = frozenset()

_TEMPLATE_HEADING = "## 5. Coordinator brief template"


def _contract() -> str:
    return Path(_THIS.CONTRACT_PATH).read_text(encoding="utf-8")


def _check_rule(text: str, rule: str) -> None:
    ident, phrases = RULE_PHRASES[rule]
    for phrase in phrases:
        assert phrase in text, f"{rule}: missing phrase {phrase!r}"
    if ident is not None:
        assert any(
            ident in line and phrases[0] in line for line in text.splitlines()
        ), f"{rule}: {ident} is not stated on the line carrying {phrases[0]!r}"


def _check_never_as_worker(text: str) -> None:
    lines = [ln for ln in text.splitlines() if "**Never-as-worker list**" in ln]
    assert len(lines) == 1, "the never-as-worker list must be one term line"
    for cmd in NEVER_AS_WORKER:
        assert re.search(rf"`{re.escape(cmd)}`", lines[0]), (
            f"{cmd} missing from the never-as-worker list"
        )


def _template_lines(text: str) -> list:
    assert _TEMPLATE_HEADING in text, "brief template section is missing"
    section = text.split(_TEMPLATE_HEADING, 1)[1]
    return section.splitlines()


def _check_guard_before_command(text: str) -> None:
    lines = _template_lines(text)
    guard = [i for i, ln in enumerate(lines) if ln.strip() == GUARD_LINE]
    command = [i for i, ln in enumerate(lines) if ln.startswith("Command:")]
    assert guard, "the brief template does not carry the guard line word for word"
    assert command, "the brief template has no Command: line"
    assert guard[0] < command[0], (
        "the guard line must come before the first Command: line"
    )


# `--run-hooks` is Orca's legacy alias for `--setup run`; `--setup inherit` follows the
# repository's own setup policy.
_REPO_SETUP_MARKERS = ("make sync-dev", "--setup run", "--run-hooks", "--setup inherit")
_SETUP_SKIP_RE = re.compile(r"--setup <?skip\b")


def _check_repo_setup_gated(text: str) -> None:
    """Every line naming a repository setup step carries the IronClaude gate, and every
    new-child creation line asks for skipped setup (the Codex finding on PR #368)."""
    _, phrases = RULE_PHRASES["child-setup"]
    hits = [ln for ln in text.splitlines() if any(m in ln for m in _REPO_SETUP_MARKERS)]
    assert hits, "no contract line states the child setup rule"
    for ln in hits:
        for phrase in phrases:
            assert phrase in ln, (
                f"repository setup step without its gate {phrase!r}: {ln!r}"
            )
    for ln in text.splitlines():
        if "--worktree new-child" in ln:
            assert _SETUP_SKIP_RE.search(ln), (
                f"new-child creation without --setup skip: {ln!r}"
            )


def _check_no_unattended_sections() -> None:
    have = sorted(
        p.stem
        for p in Path(_THIS.COMMANDS_DIR).glob("*.md")
        if re.search(r"^## Unattended mode\s*$", p.read_text(encoding="utf-8"), re.M)
    )
    assert set(have) == set(UNATTENDED_COMMANDS), (
        f"unexpected `## Unattended mode` sections: {have}"
    )


# --- positive checks -------------------------------------------------------


@pytest.mark.parametrize("rule", sorted(RULE_PHRASES))
def test_contract_states_rule(rule):
    _check_rule(_contract(), rule)


def test_never_as_worker_list_names_all_seven_commands():
    _check_never_as_worker(_contract())


def test_brief_template_puts_guard_line_before_first_command_line():
    _check_guard_before_command(_contract())


def test_no_command_has_unattended_mode_section_after_p0():
    _check_no_unattended_sections()


def test_every_repo_setup_line_is_gated():
    _check_repo_setup_gated(_contract())


# --- negative checks: each assertion fails when its rule is removed --------


def _patched_copy(tmp_path, monkeypatch, text: str) -> None:
    copy = tmp_path / "WORKER-CONTRACT.md"
    copy.write_text(text, encoding="utf-8")
    monkeypatch.setattr(_THIS, "CONTRACT_PATH", copy)


@pytest.mark.parametrize("rule", sorted(RULE_PHRASES))
def test_rule_check_fails_when_rule_removed(rule, tmp_path, monkeypatch):
    text = _contract()
    for phrase in RULE_PHRASES[rule][1]:
        text = text.replace(phrase, "")
    _patched_copy(tmp_path, monkeypatch, text)
    with pytest.raises(AssertionError):
        _check_rule(_contract(), rule)


@pytest.mark.parametrize(
    "ungated",
    [
        "- If that setup does not run `make sync-dev`, the coordinator runs it before dispatch.",
        "- A child is dispatched only after its setup has succeeded (`--setup run`).",
        "- a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>`.",
        "- a child created with `worker-start --worktree new-child`; skip nothing.",
        "- A child is created with `--run-hooks` before dispatch.",
        "- A child is created with `--setup inherit` before dispatch.",
    ],
)
def test_repo_setup_gate_check_fails_on_ungated_line(ungated, tmp_path, monkeypatch):
    _patched_copy(tmp_path, monkeypatch, _contract() + "\n" + ungated + "\n")
    with pytest.raises(AssertionError):
        _check_repo_setup_gated(_contract())


@pytest.mark.parametrize("cmd", NEVER_AS_WORKER)
def test_never_as_worker_check_fails_when_command_removed(cmd, tmp_path, monkeypatch):
    lines = _contract().splitlines()
    lines = [
        ln.replace(f"`{cmd}`", "") if "**Never-as-worker list**" in ln else ln
        for ln in lines
    ]
    _patched_copy(tmp_path, monkeypatch, "\n".join(lines))
    with pytest.raises(AssertionError):
        _check_never_as_worker(_contract())


def test_guard_order_check_fails_when_guard_follows_command(tmp_path, monkeypatch):
    head, section = _contract().split(_TEMPLATE_HEADING, 1)
    lines = section.splitlines()
    guard = next(i for i, ln in enumerate(lines) if ln.strip() == GUARD_LINE)
    moved = lines.pop(guard)
    command = next(i for i, ln in enumerate(lines) if ln.startswith("Command:"))
    lines.insert(command + 1, moved)
    _patched_copy(tmp_path, monkeypatch, head + _TEMPLATE_HEADING + "\n".join(lines))
    with pytest.raises(AssertionError):
        _check_guard_before_command(_contract())


def test_guard_order_check_fails_when_guard_line_removed(tmp_path, monkeypatch):
    head, section = _contract().split(_TEMPLATE_HEADING, 1)
    _patched_copy(
        tmp_path,
        monkeypatch,
        head + _TEMPLATE_HEADING + section.replace(GUARD_LINE, ""),
    )
    with pytest.raises(AssertionError):
        _check_guard_before_command(_contract())


def test_unattended_section_check_fails_on_unlisted_command(tmp_path, monkeypatch):
    cmds = tmp_path / "commands"
    cmds.mkdir()
    (cmds / "scratch.md").write_text(
        "# scratch\n\n## Unattended mode\n\nnone\n", encoding="utf-8"
    )
    monkeypatch.setattr(_THIS, "COMMANDS_DIR", cmds)
    with pytest.raises(AssertionError):
        _check_no_unattended_sections()


# --- AC-0.9: git and GitHub write-verb audit -------------------------------
#
# Scans the installed primitives' source for git and gh write verbs. The hit
# unit is one matching line, keyed by repo-relative path, verb(s) and the
# stripped line text (never a line number). Every hit must be classified into
# exactly one category with a one-line reason:
#   wc9-allowed      allowed by WC-9 (/sc:implement's private-index snapshot, refs, revert)
#   deferred:<phase> the owning command is converted, or its write turned off under
#                    --unattended, in that phase of ./source.md section 6
#   never-worker     the owning command is on the never-as-worker list
#   no-command       no command converts this file; the reason says why
#   read-only        a read-only use or a false match (gh pr view/list/checks, a
#                    GET gh api call, or prose that forbids or describes the verb)
# WC-9's "a worker writes no git state" covers only the hits classified here.

AUDIT_ROOTS = (
    _REPO / "src" / "superclaude" / "skills",
    _REPO / "src" / "superclaude" / "commands",
    _REPO / "src" / "superclaude" / "agents",
)

# Whole words, not followed by a word character or "-", so `git merge-base`
# is not `git merge`. `git -C <path> <verb>` counts as `git <verb>`.
WRITE_VERB_RE = re.compile(
    r"\b(?:git(?:\s+-C\s+\S+)?\s+(?:add|commit|push|merge|stash|update-ref|worktree\s+(?:add|remove))"
    r"|gh\s+(?:pr|api))(?![\w-])"
)

_CATEGORY_RE = re.compile(
    r"^(?:wc9-allowed|deferred:P[1-4]|never-worker|no-command|read-only)$"
)

# A gh api call is a post when its method is not GET: an explicit non-GET
# method, or (no explicit GET and) a field flag or graphql, which make gh use POST.
_GH_API_METHOD_NOT_GET = re.compile(r"(?:--method|-X)\s+(?!GET\b)[A-Za-z]+")
_GH_API_METHOD_GET = re.compile(r"(?:--method|-X)\s+GET\b")
_GH_API_POST_HINT = re.compile(
    r"(?:^|\s)(?:-f|-F|--field|--raw-field|--input)(?=\s|=|$)|\bgh\s+api\s+graphql\b"
)


def _is_gh_api_post(line: str) -> bool:
    if not re.search(r"\bgh\s+api\b", line):
        return False
    if _GH_API_METHOD_NOT_GET.search(line):
        return True
    return not _GH_API_METHOD_GET.search(line) and bool(_GH_API_POST_HINT.search(line))


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(_REPO).as_posix()
    except ValueError:
        return path.relative_to(root.parent).as_posix()


def _scan_write_verbs() -> list:
    """Return (path, verb, stripped line, line number) for every hit line."""
    hits = []
    for root in map(Path, _THIS.AUDIT_ROOTS):
        for p in sorted(root.rglob("*")):
            if not p.is_file():
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for n, line in enumerate(text.splitlines(), 1):
                found = WRITE_VERB_RE.findall(line)
                if not found:
                    continue
                verbs = []
                for m in found:
                    verb = re.sub(r"\s+", " ", re.sub(r"\s+-C\s+\S+", "", m))
                    if verb not in verbs:
                        verbs.append(verb)
                hits.append((_rel(p, root), "+".join(verbs), line.strip(), n))
    return hits


def _check_all_classified() -> None:
    missing = sorted(
        {(path, verb, line) for path, verb, line, _ in _scan_write_verbs()}
        - set(WRITE_VERB_CLASSIFICATION)
    )
    assert not missing, "unclassified git/gh write-verb hits:\n" + "\n".join(
        f"{p} [{v}] {ln[:120]}" for p, v, ln in missing
    )


# (repo-relative path, verb(s), stripped line) -> (category, one-line reason)
WRITE_VERB_CLASSIFICATION = {
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        '- **Wave 0 (all ordinals):** resolve the target repo once from the origin remote (`REPO="$(git remote get-url origin | sed -E \'s#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\\.git$##\')"`; only if origin has no URL, fall back to `gh repo view --json nameWithOwner -q .nameWithOwner` — never prefer it, because gh picks an `upstream` remote over `origin`) and the base branch (`gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`). BEFORE creating anything: confirm `git remote -v` shows origin = `$REPO` and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not rebase and does not halt: the branch is already published when `gh pr create` runs, so report how many commits it is behind, a Tier 0 result; with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). At L1+, also before creating or attaching, run `scripts/probe-merge.sh --ops-only --repo "$REPO"`: a non-null `foreign_op` (a merge, rebase, cherry-pick, revert or sequencer operation in progress) → HALT before Wave 1 with status `terminal_halted`, reason `foreign_op_in_progress`, nothing created (on `--resume`, `conflict_resume_plan` in `refs/conflict-mechanical.md` decides first). Then open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."` and verify the returned URL\'s `owner/repo` equals `$REPO` (a misroute → HALT). With `--pr <N>`, skip `gh pr create` and attach to that PR instead, checking the URL from `gh pr view <N> --repo "$REPO" --json url`. Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        '- **Wave 0 conflict check (L1+ only; L0 skips it):** after the head binding, read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus` (re-read an `UNKNOWN` up to 3 times, 10 s apart) and normalise it with `superclaude.pr_submit.conflicts.mergeability_hint`. Only `conflicting` or a persistent `unknown` loads `refs/conflict-mechanical.md` and runs `scripts/probe-merge.sh`; follow that ref to classify, print the plan before any edit, and route with `conflict_action(hook="wave0")` (Tier 3 at L3 halts here: `terminal_halted`, reason `conflict_tier3`, nothing touched). Any other hint is Tier 0: report "<N> commits behind, no conflicts" (or the `BLOCKED` reason) and continue; no ref is loaded.',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        "- **Wave 0 head binding (L1+ only; L0 skips it):** after `gh pr create`, or on `--pr <N>` attach, read the PR head with `gh pr view <N> --repo \"$REPO\" --json headRefName,headRefOid,isCrossRepository` (a failed or unparsable read → HALT) and the checkout with `git branch --show-current` and `git rev-parse HEAD`. Require `superclaude.pr_submit.fsm.pr_head_ok(local_branch, local_sha, headRefName, headRefOid, isCrossRepository, allow_cross_repo=(ordinal < 3))`; a head on a fork is allowed only below L3, where nothing is pushed. False → HALT before Wave 1 with status `terminal_halted`, reason `pr_head_mismatch` (appended to the run-log when one exists), and tell the operator: \"PR #<N>'s head `<headRefName>`@<headRefOid> does not match your checkout `<local_branch>`@<local_sha>. Do not close the PR. Check out `<headRefName>` and make it equal the PR head (push if you are ahead; `git pull --ff-only` if you are behind; this skill never rewrites a published branch), then re-run with `--pr <N>`.\" True → bind `HEAD_BRANCH := headRefName` and `pre_push_sha := headRefOid` for the whole run; every push targets `HEAD_BRANCH`, never the checkout's branch name. `--resume` repeats this binding against the live PR: when crash recovery finds a dangling `push_initiated`, check only the branch (`pr_branch_ok(local_branch, headRefName, isCrossRepository, allow_cross_repo=(ordinal < 3))` and `pr_branch_ok(<the record's target_branch>, headRefName, False)`), leave the SHA to `resolve_crash_window` (local HEAD may already be the fix commit), and set `pre_push_sha` from that record: its `target_sha` when the push landed (Branch A), its `pre_push_sha` when the push is re-driven (Branch B: skip the Wave 6 fix commit, set `target_sha` from the record, and the re-driven push first runs the Wave 6 pre-push head guard with the record's `pre_push_sha`; after Branch A, the guard's parent check stops the next push if local commits were made since the landed push); otherwise require the full `pr_head_ok` and set `pre_push_sha := headRefOid`.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        '- **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave 8):** read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRepository` (same `UNKNOWN` re-reads). Only `conflicting` or a persistent `unknown` loads `refs/conflict-mechanical.md`, re-probes and acts on `conflict_action(hook="wave8a", entering=<review outcome>)`: at L3 a Tier 1 conflict becomes one sync merge commit pushed fast-forward (no round, no re-trigger, no reply, no resolve; the one push a wait-only path allows), then the CI wait runs on the new head with `expect_checks`; L2 leaves it resolved and validated but uncommitted (`halt_before_push`, only after `clean` / `REPORT_ONLY`); L1 proposes (also only after `clean` / `REPORT_ONLY`). A PR still conflicting with nothing pushed skips the CI wait with reason `pr_conflicting` (GitHub runs no `pull_request` checks on it) and ends with the status `conflict_action` returns. When any hook this run read `conflicting`, re-read `mergeable` before sending `transition(clean)`; `CONFLICTING` → `terminal_halted`, reason `late_conflict` (late re-sync: #361).',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "git add+git commit+gh pr+git push+gh api",
        '- **Wave 6 (L3 only):** load `refs/thread-reply.md`. **Fix commit:** when the cycle applied edits (`applied_edits > 0`) and VAL is green, commit all of them as exactly one commit (one per cycle, never one per finding; VAL has already passed, so a validation retry never adds a second commit), staging only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`, which would sweep in run artifacts and other untracked files) and committing with `git commit --only -- <paths>` so nothing else already in the index is committed, and set `target_sha := git rev-parse HEAD`; every thread replied to in this cycle cites that one SHA. Before staging anything (before the `git add` above), if a path to commit is in `OPERATOR_PENDING`, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing committed or pushed, and tell the operator: "The fix touched files that had your own uncommitted changes: <paths>. Nothing was committed or pushed. Those files now hold both your changes and the fix: separate them by hand (do not discard the files), then re-run with `--pr <N>`." Otherwise, if the commit fails (for example a pre-commit hook rejects it) or HEAD did not advance, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing pushed, and tell the operator: "The fix commit failed (<error>). Nothing was pushed; the edits, and any changes a hook made, are in your working tree. Fix the cause, then either commit and push the fix yourself or discard it, and re-run with `--pr <N>`." A halted cycle replies to and resolves no thread. A crash re-drive (Branch B) skips this step and pushes the record\'s `target_sha`. **Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`. Compare the stored `pre_push_sha`, never local HEAD (local HEAD is the new fix commit). False → append `terminal_halted` (reason `pr_head_mismatch`), HALT with nothing pushed, write no push record, and tell the operator: "PR #<N>\'s head moved from <pre_push_sha> to <headRefOid> (or its branch is no longer `<HEAD_BRANCH>`) during the run. Nothing was pushed. Review the new PR commits, make your checkout equal the new PR head, then re-run with `--pr <N>`." When this cycle made a fix commit, the message adds: "This cycle\'s fixes are in local commit <target_sha>: drop it, or rebase it onto the new head and push it yourself." Next, when the cycle applied edits (a zero-edit cycle has no fix commit; INV-016 predicate 5 blocks its push and still records `push_decision`), read the parents of the commit to push (`git rev-list --parents -n 1 <target_sha>`, dropping the first id) and require `superclaude.pr_submit.fsm.push_parent_ok(<parents>, pre_push_sha)`: a fast-forward push publishes every commit between the PR head and `target_sha`, so the push may carry only this cycle\'s fix commit. False → append `terminal_halted` (reason `push_range_mismatch`), HALT with nothing pushed and no push record, and tell the operator: "Nothing was pushed. The fix commit <target_sha> sits on top of local commits that are not on PR #<N>: <`git log --oneline <pre_push_sha>..<target_sha>^`>. Publish those commits yourself if you want them on the PR, otherwise drop them; make your checkout equal the PR head, then re-run with `--pr <N>` (the open review threads are fixed again)." Then set `target_branch := HEAD_BRANCH`. The deterministic core DECIDES (evaluates the INV-016 conjunction, records the write-ahead push triad `push_decision` → `push_initiated` (fsynced BEFORE the push) → `push_completed`, keyed on the PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`); the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo\'s default/protected branch, never a force push) ONLY when the conjunction holds, then set `pre_push_sha := target_sha`, then reply (citing `applied_edits` status — `applied_edits==0` says "no code change applied", never "resolved") and resolve via `scripts/reply-resolve-thread.sh` (reply FIRST, then resolve; the script finds the thread by its root comment id, so an Augment or a Codex root works the same). In a dedup group, **every verified member\'s thread** is replied to and resolved, all citing the cycle\'s one fix SHA; an unverified or Low/Nit member gets no reply and no resolve, and the report lists the group once with "flagged by: augment, codex". **S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post **one re-trigger comment per present reviewer** BEFORE re-entering the S5 poll: for each reviewer in `pending_retriggers(<run-log events>, cycle_id, <present reviewers>)` (the present reviewers that have no `rereview_requested` for this `cycle_id` yet), run `scripts/retrigger-review.sh --pr <N> --repo "$REPO" --body "<retrigger_phrase(contract, reviewer)>"` (`auggie review` for Augment, `@codex review` for Codex). The core decides whether/when to re-trigger (`do_retrigger` seam, INV-R1: at most once per push cycle, `rereview_request_count <= max_rounds`, counted per cycle, not per comment); the script does the `gh api` issue-comment POST (NFR-6). Right after each reviewer\'s successful POST, take that reviewer\'s UTC watermark and append a **`rereview_requested{cycle_id, reviewer, timestamp}`** run-log event with that time (the INV-R1 producer — folded into `rereview_request_count` by distinct `cycle_id` in `rebuild_state`, and consumed by crash recovery\'s OQ-1 resume decision: a landed-push crash with NO `rereview_requested` for its cycle resumes at `S5a_RETRIGGER_REVIEW` to re-post; one WITH it resumes at `S5_AWAITING_REREVIEW`). **Resume of a re-triggered cycle:** reuse the `cycle_id` of the dangling push record (never a new one); on every resume at `S5a_RETRIGGER_REVIEW` or `S5_AWAITING_REREVIEW`, first call `pending_retriggers` and post the reviewers still missing (a crash between the Augment and the Codex post neither skips Codex nor re-posts Augment), then take each reviewer\'s watermark from the `timestamp` of its latest `rereview_requested` for the cycle before the S5 poll. The `round_counter` ticks only when the subsequent poll attributes the re-review to our pushed SHA (the relocated INV-001 increment) — a timed-out re-trigger does NOT advance the counter.',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/commits/<sha>/check-runs --jq .total_count",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/commits/<sha>/status --jq .total_count",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh pr",
        "No `conclusion` field — `gh pr checks --json` does not emit it. Empty, malformed, or multiple-document stdout is **not** a parsed empty array. A valid nonempty required list takes precedence; otherwise a valid all-checks list is used. If the chosen list is empty and either query failed to parse, emit `state:polling`, `checks:[]`; only two parsed empty arrays, with `expect_checks` false, justify `clean`; with `expect_checks` true an empty chosen list is `polling` (see Expected checks after a push). Pending exit 8 may still contain valid JSON — keep it.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md",
        "git add",
        "git add -- <path>",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh api",
        'gh api "repos/${REPO}/commits/<base_sha>/check-runs" --jq \'.check_runs[] | "\\(.name) \\(.conclusion)"\'',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRepository',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json mergeStateStatus',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json mergeable',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        '| `resume_unrepresentable` (row 4b\') | `--resume` with an open conflict cycle whose dangling push no crash record matches | The merge commit `<target_sha>` of cycle `<cycle_id>` may or may not be on the PR. Nothing more was pushed. If the PR head (`gh pr view <N> --repo "$REPO" --json headRefOid`) equals it, re-run with `--pr <N>`; otherwise push or drop it yourself, then re-run. |',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git add",
        "- Tier 2: follow `refs/conflict-intent.md` (Tier 2 only), one file at a time (J-40), staging each finished path with `git add -- <path>` or `git rm -- <path>` (J-56); then any `regen:*` path by its rule above, after the precheck. A Tier 2 halt condition: abort, `sync_tier3`.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git add",
        "git add -- uv.lock",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git commit+git merge",
        '**Step 8. L2 stops here** (`resolve_local`): append `sync_concluded{left_in_progress}`, status `halt_before_push`, and print: "The merge of `origin/<base>`@<base_sha> is resolved and validated but not committed. Review it, then run `git commit` yourself and push; or `git merge --abort`."',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git merge",
        "git merge --abort",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git push",
        "git push origin <target_sha>:<HEAD_BRANCH>",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh",
        "git commit",
        'if ! git commit -F "$MESSAGE_FILE" >"$TMP/commit.out" 2>&1; then',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh api",
        'RUNS="$(gh api "repos/${REPO}/commits/${EVIDENCE_SHA}/check-runs?per_page=1" --jq .total_count 2>/dev/null)" || RUNS=""',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh api",
        'STATUSES="$(gh api "repos/${REPO}/commits/${EVIDENCE_SHA}/status" --jq .total_count 2>/dev/null)" || STATUSES=""',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        "#           repo, or `gh pr checks --json` support, which evidence mode skips).",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "| **PR** | `<PR-num>` or `<PR-URL>` | `gh pr view <id> --json number,headRefName,baseRefName,headRepository,headRepositoryOwner,title,body,files` |",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "| `pr_review_url` | string | URL of the posted `gh pr review` comment (empty if `--no-post-pr` or non-PR target) |",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is turned off under --unattended in P2 (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- PR: fetch `gh pr view <id> --json number,headRefName,baseRefName,title,body,files,url,headRepositoryOwner,headRepository` and the merge-base diff range",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- PR: `gh pr diff <id>` → `<output-dir>/diff.patch`",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- PR: from the `files` field of `gh pr view`",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- Summary comment: `gh pr review <PR> --comment --body-file <output-dir>/REVIEW.md`",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is turned off under --unattended in P2 (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh api",
        "gh api repos/<owner>/<repo>/pulls/<PR>/comments \\",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is turned off under --unattended in P2 (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- Capture the review URL from `gh pr view <PR> --json reviews -q '.reviews[-1].url'` and record it.",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- Use `gh pr review --approve` or `--request-changes` — strictly `--comment`",
    ): (
        "read-only",
        "false match: forbids gh pr review --approve/--request-changes; no write",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "| `gh pr review` post fails | Save the body to `<output-dir>/REVIEW.md`, surface the path to the user, status `partial` | None |",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is turned off under --unattended in P2 (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md",
        "gh pr",
        "This recommendation is the report's first-paragraph verdict. It does NOT translate into a `gh pr review --approve` or `--request-changes` — those decisions belong to the human. The report is always posted as a `--comment` review.",
    ): (
        "read-only",
        "false match: states the report never becomes gh pr review --approve/--request-changes",
    ),
    (
        "src/superclaude/skills/sc-crash-recovery/SKILL.md",
        "git stash",
        "allowed-tools: Read, Glob, Grep, Bash(ls *), Bash(find *), Bash(wc *), Bash(cat *), Bash(head *), Bash(tail *), Bash(stat *), Bash(git status *), Bash(git diff *), Bash(git log *), Bash(git stash *), Bash(git branch *), Bash(git ls-files *), Bash(~/.claude/skills/sc-crash-recovery/scripts/*), Bash(~/workspace/IronClaude/.claude/skills/sc-crash-recovery/scripts/*), Task",
    ): (
        "no-command",
        "sc-crash-recovery has no /sc: command to convert; this is its tool allowlist (Bash(git stash *)), used for read-only stash inspection",
    ),
    (
        "src/superclaude/skills/sc-crash-recovery/SKILL.md",
        "git commit",
        '- **No artifacts found anywhere**: say so plainly. "No in-flight pipeline state detected. Most recent activity: <last git commit / last session log timestamp>." Don\'t fabricate work.',
    ): (
        "read-only",
        "false match: prose naming the last git commit as a timestamp source",
    ),
    (
        "src/superclaude/skills/sc-crash-recovery/refs/investigators.md",
        "git stash",
        "- git -C <PROJECT_PATH> stash list",
    ): ("read-only", "git stash list only reads the stash"),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git stash",
        "Else snapshot HEAD + tracked diffs + untracked (non-ignored) files **without** staging in the user index (`git stash create` omits untracked):",
    ): (
        "wc9-allowed",
        "/sc:implement private-index snapshot or refs/superclaude/implement/ ref, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git add",
        '`idx=$(mktemp); GIT_INDEX_FILE="$idx" git read-tree HEAD && GIT_INDEX_FILE="$idx" git add -A && start=$(GIT_INDEX_FILE="$idx" git write-tree); rm -f "$idx"`',
    ): (
        "wc9-allowed",
        "/sc:implement private-index snapshot or refs/superclaude/implement/ ref, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git update-ref",
        '`git update-ref "refs/superclaude/implement/<slug>/T<id>" "$start"` (managed: `<slug>` is the package id)',
    ): (
        "wc9-allowed",
        "/sc:implement private-index snapshot or refs/superclaude/implement/ ref, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git update-ref",
        "On task `complete`, delete the Q0 pin `git update-ref -d \"refs/superclaude/implement/<slug>/T<id>\"` and the task's checkpoint refs (`refs/retry.md`); keep its sweep refs. The final summary lists each kept sweep ref with one `git update-ref -d <ref>` line for the operator. The task's reviewed-tree refs `retry/T<rid>/r<k>-<j>` (`refs/qa.md`) are deleted at `complete` once `first=` and `origin=` are written; sweep refs are kept.",
    ): (
        "wc9-allowed",
        "/sc:implement private-index snapshot or refs/superclaude/implement/ ref, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git add",
        'Untracked files in the touched set are part of the review package: if the path exists in `$start`, diff vs `git show "$start:<path>"`; else include full new-file contents (`git diff --no-index -- /dev/null <file>` or Read). Do not `git add` to the user index for this snapshot (that is not the `.dev/tasks/` rule: `.dev/tasks/` is always staged, `git add .dev/tasks`). An empty `git diff` with new untracked writes is not `cannot-verify`.',
    ): (
        "deferred:P4",
        "/sc:implement is converted in P4; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/ledger.md",
        "git add",
        "One markdown file per run. Append-only. UTF-8, `\\n` endings, no wrapping of record lines. Do not `git add` a legacy ledger under `.dev/implement/`. A managed package's ledger (`<pkg>/progress.md`) sits under `.dev/tasks/`, which is always staged (`git add .dev/tasks`).",
    ): (
        "deferred:P4",
        "/sc:implement is converted in P4; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md",
        "git add",
        '- `.dev/tasks/` is always staged (`git add .dev/tasks`): the package, its `progress.md` ledger and `artifacts/` included. Never gitignore it, never leave it untracked, and never write "do not stage" about it in a ledger note or report. Staging is not committing. After the helper moves a package to `done/`, the new path needs `git add .dev/tasks` again.',
    ): (
        "deferred:P4",
        "/sc:implement is converted in P4; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        "1. **Procedure step 1, checkpoint.** From `$top` (Names), snapshot the worktree with the Q0 temp-index sequence (Q0 in `SKILL.md`) into tree `c`. Append `T<id>: retry n=<k+1> step=open checkpoint=<c> tier=<tier>`. Then `git update-ref <checkpoint ref> <c>`. No commit object is made, no git identity is needed, and no branch or index changes. The `step=open` record is written **before** `update-ref`, so a failed ref write never leaves the k = 2 failure without its feature marker (Resume row P in `refs/ledger.md`).",
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        "The checkpoint ref only pins the failed attempt's tree for recovery and for `attempt-<k>.diff`; it never drives the revert. On any resume into this escalation, re-run `git update-ref <checkpoint ref> <recorded sha>`. Every `r<k>-<j>` ref of the task is also re-pinned from its recorded tree (review header or repair `applied tree=` line, `refs/qa.md`). If the ref held another value (another linked worktree with the same slug), print `checkpoint ref moved; re-pinned to the recorded tree <sha>` and continue. If `update-ref` fails, STOP `E-RESUME-NEEDED reason=ref-failed` with no ledger line; the `step=open` record already exists, so resume retries. Halt messages print the recorded sha, not only the ref name (Halts and transient stops).",
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git add",
        '&& GIT_INDEX_FILE="$idx" git -C "$1" add -A 2>/dev/null \\',
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        'git -C "$top" update-ref "$ref" "$now" "" || { echo "sweep ref write failed: $ref" >&2; return 4; }',
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        'Before restoring, pin `now` as `refs/superclaude/implement/<slug>/retry/T<rid>/sweep-<k>-<seq>` with `git update-ref <ref> <now> ""` (create-only; `<seq>` is the next free integer). On a resumed revert, if a `sweep-<k>-*` ref exists, keep it and take a new `<seq>` only when `now` differs from it. Print the sweep ref at every revert.',
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        "At `complete`, delete the Q0 pin and the task's checkpoint refs `a<k>`, but keep its sweep refs: they are the only copy of bytes a revert replaced. The final summary lists them with one `git update-ref -d <ref>` line each for the operator. The task's reviewed-tree refs `retry/T<rid>/r<k>-<j>` (`refs/qa.md`) are also deleted at `complete` once `first=` and `origin=` are written; sweep refs are kept.",
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-post-release-protocol/SKILL.md",
        "git worktree add+git worktree remove",
        "**Anchor the scan to the tagged commit.** Once the tag is resolved, read the release's code surface **at that tag** — e.g. `git show <tag>:<path>`, `git ls-tree <tag>`, or a `git worktree add` / `git archive` checkout of the tag — rather than the current working tree. Such a checkout is made in a temporary directory and removed with `git worktree remove` after the scan. Confirm the tag actually belongs to the release lineage (`git merge-base --is-ancestor <tag> <default-branch>`); if it is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding. **Auto-detect the default branch** (e.g. `git symbolic-ref refs/remotes/origin/HEAD`) — do not assume `main`/`master`.",
    ): (
        "deferred:P4",
        "/sc:post-release is converted in P4 with every outward and git-writing step off under --unattended (decision D4)",
    ),
    (
        "src/superclaude/skills/sc-post-release-protocol/SKILL.md",
        "git add",
        "- **Never stage machine-generated / sync-output dirs** — respect whatever the host repo marks as generated or vendored (check its `.gitignore` and docs) and don't `git add` those paths. Note the convention varies: some repos gitignore such dirs, others commit them — follow the host repo's actual practice, don't assume.",
    ): (
        "deferred:P4",
        "/sc:post-release is converted in P4 with every outward and git-writing step off under --unattended (decision D4)",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        'unless both hold: (1) `gh pr checks --repo "$REPO" --help` lists `--json` (probe the installed CLI;',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        "Wave 0: Open PR + verify target   ← (no ref; gh pr create --repo, pre-PR checks)",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "git add",
        "- `git add` any `.claude/` path except `.claude/settings.json`.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "(`scripts/poll-augment-review.sh`) performs a single `gh`/`gh api` poll and emits one JSON line; the",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "> Every `gh`/`gh api` call below pins the RESOLVED `--repo <owner/repo>` (origin's `owner/repo`,",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh pr",
        "gh pr view <N> --repo <owner/repo> --json number,url,headRefName,headRefOid,baseRefName",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/pulls/<N>/reviews --method GET -F per_page=100 -F page=1",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/issues/<N>/comments --method GET -F per_page=100 -F page=1",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/pulls/<N>/comments --method GET -F per_page=100 -F page=1",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh pr",
        "gh pr view <N> --repo <owner/repo> --json number,url,headRefOid",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh pr",
        "gh pr checks <N> --repo <owner/repo> --required --json name,state,bucket,link,workflow",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh pr",
        "gh pr checks <N> --repo <owner/repo> --json name,state,bucket,link,workflow",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md",
        "gh api",
        "> **NOTE (core-purity boundary, NFR-6 / T-104, NOT T-N50).** This ref documents a `gh api …",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md",
        "gh api",
        "> seam); the `gh api` I/O lives in `scripts/retrigger-review.sh`.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md",
        "gh api",
        'gh api --method POST repos/<owner/repo>/issues/<N>/comments -f body="auggie review"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md",
        "gh api",
        "`gh api .../comments` or an upstream-parent path is a **T-104-class defect**. `gh api` takes no",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md",
        "gh pr+gh api",
        "(`--repo <owner/repo>` for `gh pr`; `repos/<owner/repo>/...` path for `gh api`; the GraphQL",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md",
        "gh api",
        'gh api --method POST repos/<owner/repo>/pulls/<N>/comments/<COMMENT_ID>/replies -f body="<reply-text>"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md",
        "gh api",
        "gh api graphql -f query='",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md",
        "gh api",
        "comment via `gh api --method POST repos/<owner/repo>/issues/<N>/comments -f body=...`),",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh pr",
        'if ! gh pr view "$PR" --repo "$REPO" \\',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh api",
        'issue) gh api "repos/${REPO}/issues/${PR}/comments" --method GET -F per_page=100 -F page="$page" ;;',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh api",
        'inline) gh api "repos/${REPO}/pulls/${PR}/comments" --method GET -F per_page=100 -F page="$page" ;;',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh api",
        'reviews) gh api "repos/${REPO}/pulls/${PR}/reviews" --method GET -F per_page=100 -F page="$page" ;;',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh api",
        "gh api graphql -f query='",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh pr",
        'if ! gh pr view "$PR" --repo "$REPO" --json headRefOid > "$_tmp/head.json" 2>/dev/null \\',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'CHECKS_HELP="$(gh pr checks --repo "$REPO" --help 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        "*) die \"installed gh lacks 'gh pr checks --json' (see 'gh --version'); upgrade gh and confirm via 'gh pr checks --help' before CI wait\" 2 ;;",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'PR_JSON="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        "# gh pr checks exits 8 on pending while still printing JSON. Do not `|| echo '[]'`",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'REQUIRED_JSON="$(gh pr checks "$PR" --repo "$REPO" --required --json "$JSON_FIELDS" 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'ALL_JSON="$(gh pr checks "$PR" --repo "$REPO" --json "$JSON_FIELDS" 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'PR_AFTER="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh",
        "gh api",
        "#           isolated here (NFR-6). gh api paths pin the RESOLVED repos/${REPO}/...",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh",
        "gh api",
        "gh api graphql -f query='",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh",
        "gh api",
        'gh api --method POST "repos/${REPO}/pulls/${PR}/comments/${COMMENT_ID}/replies" \\',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh",
        "gh api",
        "#           All gh I/O is isolated here (NFR-6). The gh api path pins the RESOLVED",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh",
        "gh api",
        "gh api --method POST \\",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git worktree add",
        "2. **STOP-on-non-committable predicate (COR-1)** — `committable = base resolves AND HEAD resolves AND not audit_tree_dirty`. If NOT committable, the wrapper STOPs with `status: stopped-precondition` (verdict BLOCKED, exit 2 — the fail-closed contract is unchanged) and `reason ∈ {dirty, no-committable-ref, head-moved-precondition, snapshot-precleanup-failed, worktree-add-failed}` (any non-zero `git worktree add` exit STOPs with the captured stderr, never falling back to the live tree). It never points reviewers at a committed-ref snapshot that omits the uncommitted target.",
    ): (
        "deferred:P2",
        "/sc:reflect review-snapshot worktree; reflect is converted in P2, when its git writes under --unattended are resolved",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git worktree add",
        "3. **Snapshot creation (COR-2 / A-2)** — on the committable path, pre-clean a leftover `<output>/_review-snapshot`, re-resolve HEAD immediately before `git worktree add --detach <output>/_review-snapshot <ref>` and STOP `head-moved-precondition` on drift (the parallel-session HEAD-moved hazard), then create a REAL worktree checkout (NOT an archive, so auggie stays indexed).",
    ): (
        "deferred:P2",
        "/sc:reflect review-snapshot worktree; reflect is converted in P2, when its git writes under --unattended are resolved",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git worktree remove+git stash",
        "5. **`finally` teardown (A-3)** — the snapshot is always removed via `git worktree remove --force` (never `rm -rf` / `git stash`), on success / STOP / exception, while the always-write sidecar still emits inside the try.",
    ): (
        "deferred:P2",
        "/sc:reflect review-snapshot worktree; reflect is converted in P2, when its git writes under --unattended are resolved",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git commit+git push+git stash+git merge",
        "**No-mutation gate.** Independently of (b)/(c), any command matching the mutation denylist (`git commit`/`git push`, the read-but-forbidden working-tree git verbs `git reset` / `git stash` / `git checkout` / `git clean` / `git rebase` / `git merge` / `git worktree` / `git restore` — i.e. `git <any mutation>` as a broad backstop — `pip install`, `rm`, or any redirect to a repo path outside `<output>/`) is rejected with `verify_blocked_reason: \"mutation-denied\"` and never invoked. In-test side effects (a test that writes fixtures within its own scope) are best-effort only (OQ-M7) — the gate governs the *command*, not the test internals. **(L3 defense-in-depth — NOT the incident vector.)** These git verbs are enumerated as a backstop only: control (b)'s verb allowlist is a CLOSED set (`{pytest, ruff, mypy, make, uv, npm, tsc, cargo}`) that already rejects EVERY git verb because `git` is absent from it, so no git command can reach this gate through the orchestrator's verification call. The reflect-reviewer mutation incident vector traveled the **reviewer-persona Bash-tool / L1** path (all-tools reviewer personas), which L1 + L2 close; §6.1.1 governs only the orchestrator-driven verification call, so this denylist extension is strictly defense-in-depth and does not by itself close the incident vector.",
    ): ("read-only", "false match: lists git verbs the no-mutation gate denies"),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git add",
        "**Git status.** Reflect does NOT `git add` moved files. Operator stages and commits. The `task` adapter moves folders under `.dev/tasks/`, which is always staged (`git add .dev/tasks`): re-stage it after the move.",
    ): (
        "read-only",
        "false match: states reflect does not run git add or must stop on git add -f; staging is the operator's",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git add",
        "- **`git add` after promotion.** Filesystem-level move only; the operator stages and commits.",
    ): (
        "read-only",
        "false match: states reflect does not run git add or must stop on git add -f; staging is the operator's",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git add",
        "**The `-f` rule (CLAUDE.md ABSOLUTE).** If `git add` requires `-f` on any `.claude/` path (except `.claude/settings.json`), that `-f` is the violation siren. STOP. Move the change to `src/superclaude/`, run `make sync-dev`, stage only the `src/` side. See memory `feedback_claude_dir_gitignored.md`.",
    ): (
        "read-only",
        "false match: states reflect does not run git add or must stop on git add -f; staging is the operator's",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "If `git add` requires `-f` on **any** `.claude/` path (except `.claude/settings.json`), STOP. The `-f` is the violation siren — it means you are about to commit `.claude/{skills,commands,agents,hooks,templates}/*` content, which is **gitignored sync-dev output** of `src/superclaude/`.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "1. STOP the `git add -f` attempt. Do not retry with `-f` removed against the same path.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "**Why the `-f` is the signal:** A successful `git add` against a `.claude/` path means the file was either (a) already tracked from before the gitignore landed, or (b) staged with `-f`. Case (a) is grandfathered; case (b) is the violation. The `-f` flag is the only signal that distinguishes the two at staging time, which is why this rule lives at the CLAUDE.md level and not just in a pre-commit hook — the hook catches commits, not stages, and the human eye must catch the `-f` before it gets that far.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "- Task-file instructions that name `.claude/` staging steps. If a task file says `git add .claude/skills/foo/`, the task file itself is wrong — escalate to fix the task file, do not follow it.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "- **`.gitignore`** — catches any workspace that bypassed the hook (e.g., out-of-band file creation). Such a workspace cannot be staged without `git add -f`, which then triggers the `-f` rule above.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "5. **Stage ONLY `src/` and `.dev/` paths.** NEVER stage `.claude/` paths. If `git status` shows `.claude/skills/sc-reflect-protocol/` changes after step 2, that is expected sync output — leave it unstaged. If `git add` ever requires `-f` for a `.claude/` path, apply the `-f` rule above.",
    ): (
        "no-command",
        "maintainer pre-commit procedure for editing the reflect skill in this repo; no command runs it",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git commit",
        '**`mutation-denied` (FR-4.5).** Trigger: a verification command matched the no-mutation denylist (`git commit`/`push`, `pip install`, `rm`, repo-path redirect). Emits `verify_blocked: true` + `verify_blocked_reason: "mutation-denied"`; the command is never invoked.',
    ): ("read-only", "false match: lists commands the no-mutation denylist blocks"),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/promotion-adapters.md",
        "git add",
        "Reflect does NOT `git add` moved files. Operator stages and commits both the original promotion and any subsequent rollback. A `task` adapter move or rollback changes paths under `.dev/tasks/`, which is always staged (`git add .dev/tasks`).",
    ): (
        "read-only",
        "false match: states reflect does not git add moved files; the operator stages",
    ),
    (
        "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md",
        "gh api",
        "- **Verdict source**: only when the failing arm is an identified CI job, fetch the failing arm's job log to `<output-dir>/job-<id>.log` *before* reading any verdict; the verdict is the last line in that log matching the harness's result marker, never the workflow- or job-level conclusion; no marker line ⇒ `verdict: unobservable`, `status: blocked` (not a fabricated failing test result). Non-CI artifacts retain their source/run provenance and use their own result format; an absent verdict is unknown, not FAIL, and requires no job-log download. Worked example only (not a mandatory tool): `gh run view <run-id> --json jobs --jq '.jobs[]|[.databaseId,.name,.conclusion]'` then `gh api repos/<owner>/<repo>/actions/jobs/<id>/logs > <output-dir>/job-<id>.log`; marker `^RESULT:` (a `--log-failed` view is empty under continue-on-error). Validator A8 checks the log exists at finalize.",
    ): (
        "read-only",
        "gh api fetch of a CI job log or raw source file; a read, no -f/-F and no write method",
    ),
    (
        "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md",
        "gh api",
        "- Fetch verbatim: `mcp__context7__query-docs` → remote URL fetch → raw source fetch (e.g. `gh api`); paste the returned lines into `tier1-observation.md` under `## Behaviour definitions` with source coordinates; Status `fetched:<source>`",
    ): (
        "read-only",
        "gh api fetch of a CI job log or raw source file; a read, no -f/-F and no write method",
    ),
    (
        "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md",
        "gh api",
        "| `mcp__context7__query-docs` | Conditional behaviour-definition fetch before S1.6.4 pairs and Tier 1 calibration; same fallback chain as Tier 2 | ✓ when framework/library named; behaviour-definition fetch (Wave 3 step 1; fallback `WebFetch` → raw source fetch, e.g. `gh api`) | — |",
    ): (
        "read-only",
        "gh api fetch of a CI job log or raw source file; a read, no -f/-F and no write method",
    ),
    (
        "src/superclaude/skills/sc-workflow-protocol/SKILL.md",
        "git add",
        '`.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.',
    ): (
        "deferred:P1",
        "/sc:workflow is converted in P1; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
    (
        "src/superclaude/skills/task/SKILL.md",
        "git add",
        "Under the centralized path convention, each task file lives inside its own folder: `.dev/tasks/to-do/TASK-[ID]/TASK-[ID].md`. All intermediate artifacts (research, synthesis, QA reports) go into typed subfolders within that folder. The task folder is the self-contained workspace for the entire execution. `.dev/tasks/` is always staged (`git add .dev/tasks`); never gitignore it or leave it untracked. Staging is not committing.",
    ): (
        "deferred:P2",
        "the MDTM task skill runs as tdd's nested /task, converted in P2; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
    (
        "src/superclaude/skills/task-builder/SKILL.md",
        "git add",
        "Compute `<subject>` from the goal slug of the user's request using the rules in the Subject Derivation section. If no clean subject is derivable, use `general`. Create the task folder: `.dev/tasks/to-do/TASK-RF-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/` and `qa/`. For multi-track: `.dev/tasks/to-do/TASK-RF-track-T-YYYYMMDD-HHMMSS/` per track. `.dev/tasks/` is always staged (`git add .dev/tasks`); never gitignore it or leave it untracked. Staging is not committing.",
    ): (
        "deferred:P2",
        "task-builder is reached through tdd, reflect --remediate and troubleshoot --fix, converted in P2; under --unattended its staging and CLI-mode git add -A are refused (WC-9)",
    ),
    (
        "src/superclaude/skills/task-builder/SKILL.md",
        "git add",
        '- **Action**: Ensure new task artifacts are staged so the working-tree diff is complete (`git add -A`, because the wrapper\'s audit omits never-`git add`-ed files). Then emit the recursion-breaker-guarded wrapper shell-out as a single Bash command: first the §3.2 skip guard `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi`, then `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`. `{TASK_FILE}` is the absolute tasklist path (the wrapper absolutizes its positional). NO `--base` is passed: the wrapper resolves the audit base from frontmatter `start_commit` as a SINGLE ref diffed against the working tree (so uncommitted task edits ARE audited; this is why a single-ref base is correct where a `start_commit..HEAD` range would not be). Base precedence is `--base` > frontmatter `start_commit` > `git merge-base HEAD master` (contract §6). `--depth deep` is fixed (O4 (CLI mode) fixes the POST depth at `deep`, forcing Tier-2 fan-out); `--fix` runs the bounded auto-fix loop; `--promote` lets the `task` adapter move the tasklist dir to `done/` on a clean/auto-fixed PASS. Emit NO `--reflect`, NO `--max-turns`, NO `<base>..HEAD` range, and no agent-spawn directive of any kind (the gate is a flat shell-out, never a subagent, per NFR-7 it carries none of the nesting tokens). Consume the EXIT CODE: only `0` completes the gate (clean OR auto-fixed-and-verified); `10` (halted: human-required deviations / non-convergent fix loop), `11` (degraded: audit untrustworthy), and `2` (blocked: child crash / missing-or-bad contract) all FAIL -> surface the wrapper report and HALT before Update-status-to-Done. The gate uses `superclaude reflect run` and never `/sc:task`; any re-execution uses `/task`.',
    ): (
        "deferred:P2",
        "task-builder is reached through tdd, reflect --remediate and troubleshoot --fix, converted in P2; under --unattended its staging and CLI-mode git add -A are refused (WC-9)",
    ),
    (
        "src/superclaude/commands/auggie-review.md",
        "gh pr",
        "- **Remote PR**: `<PR-number>` or `<PR-URL>` (resolved via `gh pr view`)",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/commands/auggie-review.md",
        "gh pr+gh api",
        "| `--post-pr` | `true` when target is a PR | Auto-post the markdown report as a `gh pr review --comment`. Inline comments for `Critical` and `High` findings via `gh api`. **No confirmation prompt — the user opted in by invoking the command on a PR.** |",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is turned off under --unattended in P2 (WC-9)",
    ),
    (
        "src/superclaude/commands/git.md",
        "git commit",
        "/sc:git commit --smart-commit",
    ): (
        "never-worker",
        "/sc:git is on the never-as-worker list; its commit and merge examples run only in the coordinator or person session",
    ),
    (
        "src/superclaude/commands/git.md",
        "git merge",
        "/sc:git merge feature-branch --interactive",
    ): (
        "never-worker",
        "/sc:git is on the never-as-worker list; its commit and merge examples run only in the coordinator or person session",
    ),
    (
        "src/superclaude/commands/pr-submit.md",
        "gh pr",
        "**STOP** if `--monitor >= 1` and the CI-wait preflight fails: `gh pr checks --repo <owner/repo> --help` must list `--json`, and the runtime must import `superclaude.pr_submit.ci`. The skill's CI-wait preflight is authoritative.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
}


def test_every_write_verb_hit_is_classified():
    _check_all_classified()


def test_classification_table_has_no_stale_entries():
    live = {(path, verb, line) for path, verb, line, _ in _scan_write_verbs()}
    stale = sorted(set(WRITE_VERB_CLASSIFICATION) - live)
    assert not stale, "classified lines no longer present:\n" + "\n".join(
        f"{p} [{v}] {ln[:120]}" for p, v, ln in stale
    )


@pytest.mark.parametrize(
    "key", sorted(WRITE_VERB_CLASSIFICATION), ids=lambda k: f"{k[0]}:{k[1]}"
)
def test_each_classification_has_one_category_and_a_reason(key):
    category, reason = WRITE_VERB_CLASSIFICATION[key]
    assert _CATEGORY_RE.match(category), f"bad category {category!r}"
    assert reason.strip() and "\n" not in reason, "each hit needs a one-line reason"


def test_read_only_entries_are_not_gh_api_posts():
    posts = [
        k
        for k, (cat, _) in WRITE_VERB_CLASSIFICATION.items()
        if cat == "read-only" and _is_gh_api_post(k[2])
    ]
    assert not posts, f"gh api posts classified read-only: {posts}"


def test_write_verb_regex_matches_whole_words_only():
    assert not WRITE_VERB_RE.search("git merge-base master HEAD")
    assert not WRITE_VERB_RE.search("git add-on")
    assert WRITE_VERB_RE.search("git merge feature")
    assert WRITE_VERB_RE.search('git -C "$top" update-ref "$ref" "$now"')
    assert WRITE_VERB_RE.search("gh pr view 12")


def test_gh_api_post_detection():
    assert _is_gh_api_post(
        'gh api --method POST repos/o/r/issues/1/comments -f body="x"'
    )
    assert _is_gh_api_post("gh api graphql -f query='")
    assert _is_gh_api_post('gh api repos/o/r/issues/1/comments -f body="x"')
    assert not _is_gh_api_post(
        "gh api repos/o/r/pulls/1/reviews --method GET -F per_page=100"
    )
    assert not _is_gh_api_post("gh api repos/o/r/actions/jobs/1/logs")


def test_audit_fails_on_unclassified_write_verb(tmp_path, monkeypatch):
    scratch = tmp_path / "skills" / "scratch-skill"
    scratch.mkdir(parents=True)
    (scratch / "SKILL.md").write_text(
        "# scratch\n\nRun `git push origin main` when done.\n", encoding="utf-8"
    )
    monkeypatch.setattr(_THIS, "AUDIT_ROOTS", (tmp_path / "skills",))
    assert _scan_write_verbs() == [
        (
            "skills/scratch-skill/SKILL.md",
            "git push",
            "Run `git push origin main` when done.",
            3,
        )
    ]
    with pytest.raises(AssertionError, match="unclassified"):
        _check_all_classified()
