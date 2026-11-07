"""Static checks for the merge-guard protocol text (issue #375).

Covers ``refs/merge-guard.md`` (and, from the SKILL.md wiring task on, the lines that
load it): its sections, the single place a cycle id is minted, the fenced-command
rules shared with the other refs, and drift guards that tie the names used in the
text to the pure module ``superclaude.pr_submit.merge_guard``.
"""

from __future__ import annotations

import inspect
import re
from pathlib import Path

import pytest

from superclaude.pr_submit import merge_guard as mg
from tests.pr_submit.test_static_grep import _GH_CMD, _command_lines, _repo_scoped

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
REF = SKILL_DIR / "refs" / "merge-guard.md"
ALLOWED_PROGRAMS = frozenset({"git", "gh", "uv", "make", "jq"})


def _text() -> str:
    return REF.read_text(encoding="utf-8")


def _section(heading: str) -> str:
    """The ``## <heading ...>`` section up to the next ``## `` heading, as prose:
    hand-wrapping is not part of the contract, so whitespace is collapsed."""
    text = _text()
    match = re.search(rf"^## [0-9]+\. {re.escape(heading)}.*$", text, re.M)
    assert match, f"no section starting {heading!r}"
    end = re.search(r"^## ", text[match.end() :], re.M)
    body = (
        text[match.start() : match.end() + end.start()]
        if end
        else text[match.start() :]
    )
    return " ".join(body.split())


# --- file and sections ----------------------------------------------------------


def test_the_ref_exists_and_the_script_it_names_is_a_file():
    assert REF.is_file()
    assert (SKILL_DIR / "scripts" / "set-draft-state.sh").is_file()


@pytest.mark.parametrize(
    "heading", ["Engage", "Pre-push", "Release", "Exit report", "Resume"]
)
def test_the_ref_has_a_section_for_each_step(heading):
    assert _section(heading).strip()


def test_the_title_names_the_merge_guard():
    assert "merge guard" in _text().splitlines()[0].lower()


# --- the shared command rules ---------------------------------------------------


def test_fenced_commands_start_with_an_allowed_program_or_an_existing_script():
    lines = [line.strip() for _n, line in _command_lines(REF) if line.strip()]
    assert lines, "the ref has no fenced command"
    for line in lines:
        first = line.split()[0]
        if first.startswith("scripts/"):
            assert (SKILL_DIR / first).is_file(), first
        else:
            assert first in ALLOWED_PROGRAMS, line


def test_every_gh_line_of_the_ref_is_repo_scoped():
    offenders = [
        f"{number}: {line.strip()}"
        for number, line in _command_lines(REF)
        if _GH_CMD.search(line) and not _repo_scoped(line)
    ]
    assert not offenders, offenders


def test_the_ref_carries_no_source_path_python_fence_or_line_pointer():
    text = _text()
    assert "src/superclaude" not in text
    assert "```python" not in text
    assert re.search(r"\.(py|md|sh):[0-9]+", text) is None


def test_the_ref_names_no_force_or_push_form():
    """The script flips the draft flag only; the ref never tells anyone to push."""
    assert re.search(r"\bgit push\b", _text()) is None


# --- the single minting place ---------------------------------------------------


def test_the_cycle_id_is_minted_only_in_the_engage_section():
    text = _text()
    assert text.count("fix_cycle_id(") == 1
    assert "fix_cycle_id(" in _section("Engage")
    engage = _section("Engage")
    assert "single place" in engage
    assert "`fix-<n>`" in engage and "`ci-<n>`" in engage
    for event in (
        "push_decision",
        "push_initiated",
        "push_completed",
        "rereview_requested",
    ):
        assert event in engage, event


# --- the phrases the protocol must state ----------------------------------------


def test_engage_names_the_trigger_and_once_per_cycle():
    engage = _section("Engage")
    assert "Medium-or-higher routed-finding trigger" in engage
    assert "once per cycle" in engage
    assert "verified" in engage


def test_engage_failure_halts_before_any_edit_with_the_pinned_reason():
    engage = _section("Engage")
    assert (
        "`terminal_halted` reason `draft_guard_unavailable` before any edit" in engage
    )
    assert "unreadable timeline at engage" in engage


def test_unpublished_or_uncertain_exits_leave_the_pr_draft_and_report_held():
    report = _section("Exit report")
    assert "leaves the PR draft and reports `held`" in report
    assert "unpublished or uncertain work" in report
    assert "clear command" in report


def test_pre_push_halts_on_a_pr_that_is_not_open():
    pre_push = _section("Pre-push")
    assert "`OPEN`" in pre_push
    assert "`pr_not_open`" in pre_push
    assert "before `push_decision`" in pre_push
    assert "`disabled`" in pre_push


def test_release_runs_after_publication_and_before_reply_resolve_and_retrigger():
    release = _section("Release")
    assert "after `push_completed`" in release
    assert "before any reply, resolve or re-trigger" in release or (
        "before reply, resolve and the S5a re-trigger" in release
    )
    assert "`no_edits`" in release and "`pushed`" in release
    assert "Retry once" in release
    assert "`changed: false`" in release


def test_resume_runs_below_ordinal_3_and_with_the_flag_off_and_uses_published():
    resume = _section("Resume")
    assert (
        "also runs on `--resume` below ordinal 3 and with `--merge-guard off`" in resume
    )
    assert "`published`" in resume
    assert "held_cycle_published" in resume
    for branch in ("`landed`", "`not_landed`", "`ambiguous`"):
        assert branch in resume, branch
    for reason in ("`resume_reconciled`", "`not_applied`", "`ambiguous`"):
        assert reason in resume, reason
    assert "`target_sha`" in resume


def test_the_l2_line_is_not_copied_into_the_ref():
    assert "still mergeable" not in _text()


# --- drift guards against the pure module ---------------------------------------


def test_every_core_function_the_ref_names_exists_in_the_module():
    text = _text()
    names = set(
        re.findall(
            r"\b(engage_decision|release_decision|resume_decision|classify_toggles|"
            r"guard_status|fix_cycle_id|next_cycle_number|pending_requests|"
            r"held_cycle_published|fold_draft_guard)\b",
            text,
        )
    )
    assert names >= {
        "engage_decision",
        "release_decision",
        "resume_decision",
        "classify_toggles",
        "guard_status",
        "fix_cycle_id",
        "next_cycle_number",
        "pending_requests",
        "held_cycle_published",
    }
    for name in names:
        assert callable(getattr(mg, name)), name


def test_every_action_name_in_the_tables_is_a_guard_action():
    members = {member.name for member in mg.GuardAction}
    # `OPEN` is a PR state, the only other upper-case token the ref uses.
    named = set(re.findall(r"`([A-Z][A-Z_]+)`", _text())) - {"OPEN"}
    assert named, "the ref names no action"
    assert named <= members, named - members


def test_every_reason_the_ref_names_is_returned_by_the_module():
    source = Path(mg.__file__).read_text(encoding="utf-8")
    for reason in (
        "mode_off",
        "ordinal",
        "conflict_cycle",
        "pr_not_open",
        "read_failed",
        "timeline_unreadable",
        "head_mismatch",
        "push_not_completed",
        "no_edits",
        "pushed",
        "held_through_redrive",
        "ambiguous_remote_tip",
        "ownership_unproven",
        "resume_reconciled",
        "not_applied",
        "already_draft",
        "user_override",
    ):
        assert f'"{reason}"' in source, reason
        assert f"`{reason}`" in _text() or reason in _text(), reason


def test_the_ref_lists_every_guard_status_value():
    table = _section("Exit report")
    for value in ("off", "released", "held", "user_override", "unavailable"):
        assert f"| `{value}` |" in table, value


# --- the ref states what the code does (found by review) -------------------------


@pytest.mark.parametrize(
    "name", ["engage_decision", "release_decision", "resume_decision"]
)
def test_the_calls_are_written_with_keyword_arguments_that_match_the_signature(name):
    """The decision functions take keyword arguments only, so a call written
    positionally in the ref would raise TypeError; every required parameter is named."""
    function = getattr(mg, name)
    parameters = inspect.signature(function).parameters
    assert all(p.kind is inspect.Parameter.KEYWORD_ONLY for p in parameters.values())
    match = re.search(rf"`{name}\(([^`]*)\)`", " ".join(_text().split()))
    assert match, name
    written = [part.strip() for part in match.group(1).split(",")]
    assert all(part.endswith("=...") for part in written), written
    names = {part[:-4] for part in written}
    required = {
        n for n, p in parameters.items() if p.default is inspect.Parameter.empty
    }
    assert required <= names <= set(parameters), (required, names)
    assert "keyword arguments only" in _text().replace("\n", " ")


def test_resume_below_ordinal_3_reports_and_does_not_reconcile():
    """Row 2 answers before row 3, so an unsettled request is left as it is."""
    resume = _section("Resume")
    assert "row 2 below answers first" in resume
    assert "an unsettled request is not reconciled there" in resume
    assert "an unsettled request is left as it is" in resume
    assert "Unsettled requests are always reconciled first" not in _text()
    pending = [{"to": "draft", "event_type": "draft_guard_requested"}]
    guard = {
        "phase": "engage_pending",
        "owned_draft": False,
        "baseline": 0,
        "run_toggles": 0,
        "unsettled": 1,
    }
    for mode, ordinal in (("off", 3), ("draft", 2)):
        decision = mg.resume_decision(
            mode=mode,
            ordinal=ordinal,
            guard=guard,
            read=None,
            pending=pending,
            dangling_branch=None,
            published=False,
        )
        assert decision.action == mg.GuardAction.REPORT_HELD, (mode, ordinal)


def test_only_a_failed_or_incomplete_read_halts_at_engage():
    """Events missing from a complete read classify `unreadable` but do not halt engage."""
    section = _section("Foreign toggle")
    assert "only a failed or incomplete read halts" in section
    assert "events missing from a complete read are not a halt at engage" in section
    guard = {
        "phase": "engage_pending",
        "owned_draft": False,
        "baseline": 0,
        "run_toggles": 2,
        "unsettled": 0,
        "failed_mutations": 0,
    }
    complete = mg.GuardRead(
        ok=True, state="OPEN", is_draft=False, transitions=1, complete=True
    )
    assert mg.classify_toggles(guard, complete) == "unreadable"
    decision = mg.engage_decision(
        mode=mg.GuardMode.DRAFT,
        ordinal=3,
        cycle_id="fix-2",
        guard=guard,
        read=complete,
    )
    assert decision.action == mg.GuardAction.ENGAGE
    incomplete = mg.GuardRead(
        ok=True, state="OPEN", is_draft=False, transitions=None, complete=False
    )
    halted = mg.engage_decision(
        mode=mg.GuardMode.DRAFT,
        ordinal=3,
        cycle_id="fix-2",
        guard=guard,
        read=incomplete,
    )
    assert halted.action == mg.GuardAction.HALT_UNAVAILABLE
    assert halted.reason == "timeline_unreadable"


def test_a_draft_guard_unavailable_halt_reports_unavailable():
    """With no request appended (the engage read failed) the folded state is empty and
    `guard_status` says `released`, so the ref states the halt reports `unavailable`."""
    report = _section("Exit report")
    assert "reason `draft_guard_unavailable` reports `unavailable`" in report
    assert "whatever `guard_status` returns" in report
    assert mg.guard_status(None, mg.GuardMode.DRAFT, 3) == "released"


# --- the SKILL.md wiring (Wave 0 hook, flag row, output row, wave line) ----------

SKILL = SKILL_DIR / "SKILL.md"
L2_LINE = "PR #N is still mergeable; this run's fixes are local only."
OFF_LINE = "Remediation is unprotected: --merge-guard off."
WAVE0_START = "- **Wave 0 merge-guard hook"
WAVE1_START = "- **Wave 1 (L1+):**"
# The whole bullet is pinned: any added or changed wording, in the heading, the loading
# sentence or the `off` sentence, is caught without a list of words to look for.
WAVE0_HEADING = "- **Wave 0 merge-guard hook (every ordinal, both modes):**"
WAVE0_LOADING = (
    "on `--resume`, or when the run log already holds guard events "
    "(`draft_guard_requested` or `draft_guard_settled`), load `refs/merge-guard.md` "
    "(Exit report and Resume) before Wave 1 and before any edit, release or re-trigger, "
    "and follow its Resume rows with the held cycle's `target_sha`, so a PR left held "
    "by an earlier run is reported or released first."
)
WAVE0_OFF = (
    f'At L3 with `--merge-guard off`, print "{OFF_LINE}" once and make no '
    "draft-state call."
)
WAVE0_BULLET = " ".join((WAVE0_HEADING, WAVE0_LOADING, WAVE0_OFF))


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _wave0_problems(text: str) -> list[str]:
    """Everything wrong with the Wave 0 guard bullet of a SKILL.md text."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith(WAVE0_START)]
    wave1 = [i for i, line in enumerate(lines) if line.startswith(WAVE1_START)]
    if len(starts) != 1 or len(wave1) != 1:
        return ["the Wave 0 guard bullet or the Wave 1 bullet is missing or repeated"]
    bullet = lines[starts[0]]
    problems = []
    if starts[0] > wave1[0]:
        problems.append("the bullet sits after the Wave 1 bullet")
    for need in (
        "`--resume`",
        "when the run log already holds guard events",
        "before any edit, release or re-trigger",
        "`refs/merge-guard.md`",
        "`target_sha`",
        OFF_LINE,
    ):
        if need not in bullet:
            problems.append(f"the bullet lacks {need!r}")
    if bullet != WAVE0_BULLET:
        problems.append(
            "the bullet differs from the pinned ungated text (a gate or edit)"
        )
    return problems


def test_the_wave0_bullet_is_flat_early_and_ungated():
    assert _wave0_problems(_skill()) == []


def test_the_pinned_wave0_text_names_no_gate():
    """The pin itself must not be a gated bullet: strip the three parts that may name
    an ordinal, L3 or the draft events, then scan what is left."""
    assert "every ordinal, both modes" in WAVE0_HEADING
    rest = WAVE0_BULLET
    for part in (
        WAVE0_HEADING,
        WAVE0_OFF,
        "draft_guard_requested",
        "draft_guard_settled",
    ):
        assert rest.count(part) == 1, part
        rest = rest.replace(part, "")
    assert not re.search(
        r"\bL\d\b|level|ordinal|monitor|draft|mode|only|tier", rest, re.I
    ), rest


def test_the_wave0_check_fails_on_each_way_the_bullet_can_go_wrong():
    text = _skill()
    lines = text.splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith(WAVE0_START))
    wave1 = next(i for i, line in enumerate(lines) if line.startswith(WAVE1_START))
    moved = (
        lines[:index]
        + lines[index + 1 : wave1 + 1]
        + [lines[index]]
        + lines[wave1 + 1 :]
    )
    assert any("after the Wave 1" in p for p in _wave0_problems("\n".join(moved)))
    off_removed = text.replace(OFF_LINE, "")
    assert off_removed != text
    assert any("lacks" in p for p in _wave0_problems(off_removed))
    edits = [
        ("(every ordinal, both modes)", "(L3 only)"),
        ("(every ordinal, both modes)", "(draft mode)"),
        (
            "or when the run log already holds",
            "at level 3, or when the run log already holds",
        ),
        (
            "or when the run log already holds",
            "at L3, or when the run log already holds",
        ),
        (
            "or when the run log already holds",
            "when the PR is a draft, or when the run log already holds",
        ),
        (
            "or when the run log already holds",
            "with --monitor 3, or when the run log already holds",
        ),
        (
            "or when the run log already holds",
            "once the PR is marked ready for review, or when the run log already holds",
        ),
        ("At L3 with", "At L3 in draft mode with"),
    ]
    for old, new in edits:
        assert old in text, old
        gated = text.replace(old, new, 1)
        assert gated != text, new
        assert any("gate" in p for p in _wave0_problems(gated)), new
    # Every word position of the real bullet, heading and `off` sentence included: an
    # insertion in the first words also breaks the bullet's start, which is a problem too.
    words = WAVE0_BULLET.split(" ")
    for i in range(len(words)):
        for phrase in ("in draft mode", "at L3 only"):
            mutated = " ".join(words[:i] + [phrase] + words[i:])
            gated = text.replace(WAVE0_BULLET, mutated, 1)
            assert gated != text, (i, phrase)
            assert _wave0_problems(gated), (i, phrase)


def test_the_flag_row_follows_the_conflict_flag_and_matches_the_parser():
    from superclaude.pr_submit.fsm import build_arg_parser

    rows = [line for line in _skill().splitlines() if line.startswith("| `--")]
    names = [row.split("|")[1].strip() for row in rows]
    assert "`--merge-guard {draft,off}`" in names
    assert names.index("`--merge-guard {draft,off}`") == (
        names.index("`--conflict-max-tier {0,1,2}`") + 1
    )
    row = rows[names.index("`--merge-guard {draft,off}`")]
    assert "default `draft`" in row and "No effect below L3" in row
    action = next(
        a for a in build_arg_parser()._actions if "--merge-guard" in a.option_strings
    )
    assert list(action.choices) == ["draft", "off"]


def test_the_output_row_lists_every_status_and_carries_the_l2_line_in_skill_md():
    text = _skill()
    rows = [line for line in text.splitlines() if line.startswith("| `merge_guard` |")]
    assert len(rows) == 1
    for value in ("off", "released", "held", "user_override", "unavailable"):
        assert f"`{value}`" in rows[0], value
    assert L2_LINE in rows[0]
    assert L2_LINE in text
    assert L2_LINE not in _text()
    contract = text.index("## Output Contract")
    assert contract < text.index(rows[0]) < text.index("## Wave / Phase Structure")


def test_the_wave_structure_has_one_guard_line_before_wave_1():
    fences = _skill().split("```text")[1:]
    block = next(f for f in fences if "\nWave 0:" in f).split("```", 1)[0].splitlines()
    guard = [i for i, line in enumerate(block) if line.startswith("Wave 0d:")]
    wave1 = [i for i, line in enumerate(block) if line.startswith("Wave 1:")]
    assert len(guard) == 1 and len(wave1) == 1 and guard[0] < wave1[0]
    assert "refs/merge-guard.md" in block[guard[0]] and "--resume" in block[guard[0]]


def test_the_new_skill_lines_name_no_gh_write_no_python_and_no_second_ref_rule():
    text = _skill()
    new = [
        line
        for line in text.splitlines()
        if "merge-guard" in line or "merge_guard" in line
    ]
    assert len(new) >= 4
    for line in new:
        assert "gh pr" not in line and "gh api" not in line, line
        assert "evidence-validator" not in line and "conflict-intent.md" not in line, (
            line
        )
    assert text.count("```python") == 1
    assert "src/superclaude" not in text


# --- the Wave 3, Wave 6 and Wave 8 guard bullets and the state-machine overlay ----

STATE_MACHINE = SKILL_DIR / "refs" / "state-machine.md"
GATE = "(L3 with `--merge-guard draft` only)"
# Literal starts of the two sentences this plan must leave byte-identical (the "Pinned
# literal starts" of the pre-build record); compared as constants, not with git history.
S5A_START = (
    "**S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT "
    "auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle "
    "applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; "
    "`superclaude.pr_submit.fsm.should_retrigger`), post **one re-trigger comment per "
    "present reviewer** BEFORE re-entering the S5 poll:"
)
PREPUSH_SENTENCE = (
    "**Pre-push head guard, before `push_decision`:** re-read "
    '`gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` '
    "and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, "
    "isCrossRepository)` and `headRefName == HEAD_BRANCH`."
)
WAVE6_LINE_START = "- **Wave 6 (L3 only):**"


def _guard_bullet(text: str, wave: int) -> str | None:
    prefix = f"- **Wave {wave} merge guard "
    found = [line for line in text.splitlines() if line.startswith(prefix)]
    return found[0] if len(found) == 1 else None


def _bullet_problems(text: str, wave: int, required: tuple[str, ...]) -> list[str]:
    bullet = _guard_bullet(text, wave)
    if bullet is None:
        return [f"the Wave {wave} guard bullet is missing or repeated"]
    problems = []
    for need in (GATE, "load `refs/merge-guard.md`", *required):
        if need not in bullet:
            problems.append(f"the Wave {wave} bullet lacks {need!r}")
    return problems


WAVE3_NEEDS = (
    "At the end of Wave 3, engage the guard only when at least one verified finding "
    "of Medium severity or higher is routed to a fix",
    "the Medium-or-higher routed-finding trigger",
    "once per cycle id",
    "the single place that mints the cycle id",
    "kind `ci` for a CI-fix cycle",
)
WAVE6_NEEDS = (
    "Pre-push runs at the pre-push head guard step before `push_decision`",
    "`pr_not_open`",
    "Release runs after `push_completed`",
    "before any reply, resolve or S5a re-trigger",
    "print the clear command from the ref",
)
WAVE8_NEEDS = (
    "engages the guard with kind `ci` (cycle id `ci-<n>`)",
    "releases after `push_completed` before the CI re-poll",
)


def _case_insensitive_start(text: str, phrase: str) -> str:
    """The text with `phrase` removed once, tolerating a capital letter at its start."""
    for variant in (phrase, phrase[0].upper() + phrase[1:]):
        if variant in text:
            return text.replace(variant, "", 1)
    raise AssertionError(phrase)


@pytest.mark.parametrize(
    ("wave", "needs"), [(3, WAVE3_NEEDS), (6, WAVE6_NEEDS), (8, WAVE8_NEEDS)]
)
def test_each_guard_bullet_is_gated_and_states_its_sentences(wave, needs):
    text = _skill()
    assert _bullet_problems(text, wave, needs) == []
    bullet = _guard_bullet(text, wave)
    # The bullet is a new physical line after the pinned wave line, never inside it.
    assert bullet and bullet.startswith(f"- **Wave {wave} merge guard {GATE}:**")


@pytest.mark.parametrize(
    ("wave", "needs"), [(3, WAVE3_NEEDS), (6, WAVE6_NEEDS), (8, WAVE8_NEEDS)]
)
def test_each_guard_bullet_test_fails_when_a_phrase_or_the_bullet_is_removed(
    wave, needs
):
    text = _skill()
    bullet = _guard_bullet(text, wave)
    assert bullet
    for need in (GATE, "load `refs/merge-guard.md`", *needs):
        mutated = text.replace(bullet, _case_insensitive_start(bullet, need), 1)
        assert mutated != text, need
        assert _bullet_problems(mutated, wave, needs), need
    assert _bullet_problems(text.replace(bullet, ""), wave, needs)


def test_the_wave3_bullet_is_not_an_unconditional_engage():
    """An unconditional "engage at the end of Wave 3" must not pass the test."""
    text = _skill()
    bullet = _guard_bullet(text, 3)
    assert bullet
    unconditional = bullet.replace(
        "only when at least one verified finding of Medium severity or higher is routed to a fix",
        "",
    )
    assert unconditional != bullet
    assert _bullet_problems(text.replace(bullet, unconditional), 3, WAVE3_NEEDS)


def test_the_wave6_bullet_puts_pre_push_before_release_and_release_before_the_rest():
    bullet = _guard_bullet(_skill(), 6)
    assert bullet
    assert bullet.index("Pre-push runs") < bullet.index("Release runs")
    assert bullet.index("Release runs after `push_completed`") < bullet.index(
        "before any reply, resolve or S5a re-trigger"
    )


def test_the_wave8_text_names_the_ci_kind_and_the_ci_cycle_id():
    bullet = _guard_bullet(_skill(), 8)
    assert bullet and "kind `ci`" in bullet and "`ci-<n>`" in bullet


def test_the_s5a_and_pre_push_sentences_are_byte_identical_to_the_recorded_text():
    text = _skill()
    wave6 = [line for line in text.splitlines() if line.startswith(WAVE6_LINE_START)]
    assert len(wave6) == 1
    for sentence in (S5A_START, PREPUSH_SENTENCE):
        assert text.count(sentence) == 1, sentence[:40]
        assert sentence in wave6[0], sentence[:40]
    # The new bullet is its own line: it never sits inside the pinned Wave 6 line.
    assert "merge guard" not in wave6[0]


def test_the_state_machine_overlay_says_guard_phases_are_folded_values():
    from superclaude.pr_submit.fsm import MonitorState

    text = STATE_MACHINE.read_text(encoding="utf-8")
    start = text.index("### 5.2e Merge guard overlay")
    note = text[start : text.index("## 5.3 G-push")]
    prose = " ".join(note.split())
    assert "are not `MonitorState` members" in prose
    assert "folded values" in prose and "`refs/merge-guard.md`" in prose
    assert "never changes the FSM state" in prose
    for phase in mg.Phase:
        assert f"`{phase.name}`" in prose, phase
        assert phase.name not in MonitorState.__members__
    assert re.search(r"\bgh\b|\bgit\b", note) is None


# --- the command file (argument hint, Options row, "Merge guard" section) ---------

COMMAND = REPO_ROOT / "src" / "superclaude" / "commands" / "pr-submit.md"
CLEAR_COMMAND = 'gh pr ready <N> --repo "$REPO"'


def _command() -> str:
    return COMMAND.read_text(encoding="utf-8")


def _command_section() -> str:
    text = _command()
    start = text.index("## Merge guard")
    return " ".join(text[start : text.index("\n## ", start + 1)].split())


def test_the_command_argument_hint_names_the_flag_after_the_conflict_flag():
    hint = next(
        line for line in _command().splitlines() if line.startswith("argument-hint:")
    )
    assert "[--merge-guard {draft,off}]" in hint
    assert hint.index("--conflict-max-tier") < hint.index("--merge-guard")


def test_the_command_options_row_has_the_flag_default_and_off_line():
    rows = [
        line for line in _command().splitlines() if line.startswith("| `--merge-guard")
    ]
    assert len(rows) == 1
    row = rows[0]
    assert row.startswith("| `--merge-guard {draft,off}` | draft |")
    assert "Effective only at `--monitor 3`" in row
    assert OFF_LINE in row


def test_the_command_flag_appears_in_the_hint_the_row_and_the_section_heading():
    lines = [
        n for n, line in enumerate(_command().splitlines()) if "merge-guard" in line
    ]
    kinds = {
        "hint": any(
            _command().splitlines()[n].startswith("argument-hint:") for n in lines
        ),
        "row": any(
            _command().splitlines()[n].startswith("| `--merge-guard") for n in lines
        ),
        "heading": any(
            _command().splitlines()[n].startswith("## Merge guard") for n in lines
        ),
    }
    assert all(kinds.values()), kinds


def test_the_command_section_states_default_on_clear_command_and_unverified_gates():
    section = _command_section()
    assert section.startswith("## Merge guard (`--merge-guard`)")
    assert "on by default (`draft`) and acts only at `--monitor 3`" in section
    assert CLEAR_COMMAND in _command()
    assert "Medium severity or higher" in section and "once per fix cycle" in section
    assert "only after the cycle's fix push is confirmed" in section
    assert "`merge_guard: held`" in section
    assert (
        "never marks the PR ready" in section and "`draft_guard_unavailable`" in section
    )
    assert "release gates G4 and G5" in section
    assert "unverified until the owner's run on a disposable PR" in section
    assert "the PR body states this release gate" in section
    assert "src/superclaude" not in _command()
    assert "## Unattended mode" not in _command()


def test_the_command_clear_command_is_one_repo_scoped_fenced_line():
    fenced = [line.strip() for _n, line in _command_lines(COMMAND) if line.strip()]
    assert CLEAR_COMMAND in fenced
    assert all(_repo_scoped(line) for line in fenced if _GH_CMD.search(line))


# --- the user guides ---------------------------------------------------------------

GUIDES = REPO_ROOT / "docs" / "user-guide"


def test_the_user_guides_document_the_flag_the_clear_command_and_the_open_gate():
    commands = " ".join((GUIDES / "commands.md").read_text(encoding="utf-8").split())
    flags = (GUIDES / "flags.md").read_text(encoding="utf-8")
    assert "[--merge-guard {draft,off}]" in commands
    assert "**Merge guard:** `--merge-guard` defaults to `draft`" in commands
    assert "acts only at monitor `3`" in commands
    assert "`gh pr ready <N> --repo <REPO>`" in commands
    assert "`merge_guard: held`" in commands
    assert "unverified until the owner runs the disposable-PR gate" in commands
    assert OFF_LINE in commands
    row = next(
        line for line in flags.splitlines() if line.startswith("| `--merge-guard`")
    )
    assert "`draft` (default)" in row and "`off`" in row
    names = [
        line.split("|")[1].strip()
        for line in flags.splitlines()
        if line.startswith("| `--")
    ]
    assert names.index("`--merge-guard`") == names.index("`--conflict-max-tier`") + 1


# --- resume row 4 branches on the held cycle's push kind (review finding) ----------


def test_resume_row_4_sends_a_ci_cycle_to_the_ci_wait_and_not_to_the_re_trigger():
    """A crashed CI-fix cycle must not post review re-trigger comments: Wave 8 forbids it
    and crash recovery routes a landed `ci` push to the Wave 8 CI wait."""
    from superclaude.pr_submit.conflicts import crash_resume_plan
    from superclaude.pr_submit.models import MonitorState

    row = next(
        line
        for line in _command_section_free_resume().splitlines()
        if line.startswith("| 4 |")
    )
    row = " ".join(row.split())
    assert "branch on the held cycle's push kind" in row
    assert "A `fix` cycle runs the S5a logic of `refs/review-retrigger.md`" in row
    assert "A `ci` cycle posts no re-trigger, reply or resolve" in row
    assert "`wave8_ci_wait` plan of `crash_resume_plan`" in row
    sha = "a" * 40
    ci = {
        "kind": "ci",
        "cycle_id": "ci-1",
        "target_sha": sha,
        "review_terminal": "clean",
        "expect_checks": True,
    }
    plan = crash_resume_plan(ci, "landed", MonitorState.S5A_RETRIGGER_REVIEW)
    assert plan.directive == "wave8_ci_wait"
    fix = crash_resume_plan(
        {"kind": "fix", "cycle_id": "fix-1", "target_sha": sha},
        "landed",
        MonitorState.S5A_RETRIGGER_REVIEW,
    )
    assert fix.directive == "fsm" and fix.state == MonitorState.S5A_RETRIGGER_REVIEW


def _command_section_free_resume() -> str:
    text = _text()
    start = text.index("## 7. Resume")
    return text[start:]


def test_resume_row_3_states_the_allowance_for_earlier_failed_mutations():
    row = next(
        line for line in _text().splitlines() if line.startswith("| 3 | `RECONCILE` |")
    )
    row = " ".join(row.split())
    assert "plus up to one more for each earlier failed mutation" in row
    assert "the transition count is the run's (plus the same allowance)" in row


def test_the_engage_table_names_the_rebind_action_and_the_fold_wording():
    from superclaude.pr_submit import merge_guard as guard_module

    engage = _section("Engage")
    assert "| `REBIND` |" in engage and "`cycle_rebound`" in engage
    assert "the held guard follows the new cycle" in engage
    assert guard_module.GuardAction.REBIND.name == "REBIND"
    row = " ".join(
        next(line for line in _text().splitlines() if line.startswith("| 3 |")).split()
    )
    assert "no later settle of the same cycle and direction has resolved" in row
    assert "`changed: false` means it landed" in row
    assert "cannot be told from the request itself" in row
