"""Notes-contract tests for the /sc:issue --create question rule (issue 834).

These tests check the shipped notes template (templates/draft-notes.md) and the
rule text of refs/create.md as written. They build notes files from the real
template and count the questions the rule asks for each one. They are contract
tests: they do not prove that a model follows the rule, and a passing run is
never evidence of model behavior.
"""

import re
from pathlib import Path

import pytest

from tests.skills.test_issue_protocol import (
    CONFLICT_CATEGORIES,
    REFS,
    TEMPLATES,
    _text,
    headings,
    prompt_rule_section,
)

NOTES_TEMPLATE = TEMPLATES / "draft-notes.md"
CREATE_REF = REFS / "create.md"
NEW_MATERIAL = "New material"
CONTRADICTIONS = "Contradictions"
EMPTY_MARKER = "- None"
COMMENT = re.compile(r"(<!--.*?-->)", re.S)


def _visible(text: str) -> str:
    """The text with every HTML comment (single-line or multi-line) removed."""
    return COMMENT.sub("", text)


def _check_shape(text: str) -> None:
    found = headings(_visible(text))
    if found != [NEW_MATERIAL, CONTRADICTIONS]:
        raise ValueError(f"notes headings are {found}, not the two the rule reads")


def build_notes(
    additions: list[str], contradictions: list[str], template: str | None = None
) -> str:
    """The real notes template with the given items under each heading.

    An empty list keeps the template's `- None` marker. Raises when a heading or
    a `- None` marker of the template is missing or renamed.
    """
    text = _text(NOTES_TEMPLATE) if template is None else template
    _check_shape(text)
    items = {NEW_MATERIAL: additions, CONTRADICTIONS: contradictions}
    markers = dict.fromkeys(items, 0)
    heading = None
    parts = []
    for index, part in enumerate(COMMENT.split(text)):
        if index % 2:  # an HTML comment is kept untouched
            parts.append(part)
            continue
        lines = []
        for line in part.split("\n"):
            if line.startswith("## "):
                heading = line[3:].strip()
            if line == EMPTY_MARKER and heading in items:
                markers[heading] += 1
                if items[heading]:
                    lines.extend(f"- {item}" for item in items[heading])
                else:
                    lines.append(line)
                continue
            lines.append(line)
        parts.append("\n".join(lines))
    for name, count in markers.items():
        if count != 1:
            raise ValueError(
                f"expected one '- None' marker under {name}, found {count}"
            )
    return "".join(parts)


CATEGORY_FRAGMENTS = [name.lower() for name in CONFLICT_CATEGORIES]
SECRET_CATEGORY = "secret material"
FLAG_AS_PASSED = re.compile(r"--[a-z][a-z-]*(?: \S+)?")
QUOTED_WORDS = re.compile(r'"[^"]+"')


def contradiction_item(category: str, user_words: str, evidence: str) -> str:
    """One Contradictions line in the form these tests read: three fields.

    The shipped template names the three parts (a category, the user's own words
    in quotes or the flag as passed, and the conflicting evidence) but no field
    separator; the " | " separator is this module's own convention.
    """
    return f"{category} | {user_words} | {evidence}"


def is_supported_contradiction(item: str) -> bool:
    """Whether a Contradictions line carries all three parts the template needs.

    A line missing its category, its quoted user words (or the flag as passed) or
    its evidence belongs under New material. The secret-material exception is a
    line that names a place and never a value: it counts without user words.
    """
    fields = [field.strip() for field in re.split(r"\s*\|\s*", item)]
    if len(fields) != 3:
        return False
    category, user_words, evidence = fields
    if category.lower() == SECRET_CATEGORY:
        return evidence.startswith("place:") and len(evidence) > len("place:")
    known = any(fragment in category.lower() for fragment in CATEGORY_FRAGMENTS)
    has_words = bool(
        QUOTED_WORDS.search(user_words) or FLAG_AS_PASSED.fullmatch(user_words)
    )
    return known and has_words and bool(evidence)


def read_notes(text: str) -> tuple[list[str], list[str]]:
    """The items under New material and under Contradictions, comments ignored.

    The `None` marker is not an item. An item under Contradictions that is not a
    complete, supported contradiction (see `is_supported_contradiction`) is
    returned with the New material items, as the template says. Raises when
    either heading is missing, renamed, or joined by another heading.
    """
    visible = _visible(text)
    _check_shape(text)
    sections: dict[str, list[str]] = {}
    current = None
    for line in visible.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current and line.startswith("- "):
            item = line[2:].strip()
            if item and item != "None":
                sections[current].append(item)
    supported = [i for i in sections[CONTRADICTIONS] if is_supported_contradiction(i)]
    unsupported = [i for i in sections[CONTRADICTIONS] if i not in supported]
    return sections[NEW_MATERIAL] + unsupported, supported


def questions_for(notes_text: str) -> int:
    """Questions the shipped rule asks for a notes file: zero or exactly one.

    Only an item under Contradictions counts, however many items sit under New
    material (the rule's "Contradiction prompt rule" in refs/create.md).
    """
    _additions, contradictions = read_notes(notes_text)
    return 1 if contradictions else 0


def test_empty_notes_reproduce_the_real_template_and_read_back_empty():
    template = _text(NOTES_TEMPLATE)
    built = build_notes([], [])
    assert built == template
    assert read_notes(built) == ([], [])


def test_built_items_land_under_their_own_heading():
    complete = contradiction_item("reversed choice", '"x"', "the draft reverses x")
    notes = build_notes(["Assumption: a", "b"], [complete])
    assert read_notes(notes) == (["Assumption: a", "b"], [complete])


def test_template_property_renamed_heading_is_rejected():
    renamed = _text(NOTES_TEMPLATE).replace("## Contradictions", "## Conflicts")
    with pytest.raises(ValueError, match="notes headings"):
        build_notes([], [], template=renamed)
    with pytest.raises(ValueError, match="notes headings"):
        read_notes(renamed)


def test_template_property_deleted_none_marker_is_rejected():
    cut = _text(NOTES_TEMPLATE).replace("\n- None", "\n- ", 1)
    with pytest.raises(ValueError, match="'- None' marker"):
        build_notes([], [], template=cut)


def test_template_property_added_third_heading_is_rejected():
    added = _text(NOTES_TEMPLATE) + "\n## Extra\n\n- None\n"
    with pytest.raises(ValueError, match="notes headings"):
        build_notes([], [], template=added)
    with pytest.raises(ValueError, match="notes headings"):
        read_notes(added)


def test_template_property_item_like_comment_lines_are_ignored():
    text = _text(NOTES_TEMPLATE).replace(
        "## New material\n",
        "## New material\n\n<!--\n- a fake item\n- another\n-->\n",
        1,
    )
    assert read_notes(text) == ([], [])


def test_module_documents_its_limit_and_holds_no_copy_of_the_template():
    assert "do not prove that a model follows the rule" in " ".join(
        (__doc__ or "").split()
    )
    source = Path(__file__).read_text(encoding="utf-8")
    template_lines = [
        line for line in _text(NOTES_TEMPLATE).splitlines() if len(line) > 30
    ]
    assert template_lines
    assert [line for line in template_lines if line in source] == []


# --- the rule text that questions_for implements ------------------------------------

ZERO_QUESTIONS = "ask zero questions"
ONE_QUESTION = "ask exactly one question"
EVERY_ITEM = "naming every item"
NONE_ONLY = "notes with only `None` under both headings"
RULE_PHRASES = [ZERO_QUESTIONS, ONE_QUESTION, EVERY_ITEM, NONE_ONLY]


def rule_outcome_problems(ref: str) -> list[str]:
    """Problems with the outcomes the prompt rule section must state."""
    section = prompt_rule_section(ref)
    return [
        f"prompt rule section lacks {phrase!r}"
        for phrase in RULE_PHRASES
        if phrase not in section
    ]


@pytest.mark.parametrize("phrase", RULE_PHRASES)
def test_rule_text_states_the_outcome_questions_for_implements(phrase):
    assert phrase in prompt_rule_section(_text(CREATE_REF))


def test_rule_outcome_check_passes_on_the_shipped_rule():
    assert rule_outcome_problems(_text(CREATE_REF)) == []


def test_rule_outcome_check_fails_when_the_zero_question_phrase_is_removed():
    ref = _text(CREATE_REF)
    section = prompt_rule_section(ref)
    cut = ref.replace(section, section.replace(ZERO_QUESTIONS, "ask something"))
    assert rule_outcome_problems(cut) == [
        f"prompt rule section lacks {ZERO_QUESTIONS!r}"
    ]


def test_rule_outcome_check_fails_when_the_one_question_phrase_is_removed():
    ref = _text(CREATE_REF)
    section = prompt_rule_section(ref)
    cut = ref.replace(section, section.replace(ONE_QUESTION, "ask a question"))
    assert rule_outcome_problems(cut) == [f"prompt rule section lacks {ONE_QUESTION!r}"]


# --- question counts for each notes scenario ----------------------------------------

ADDITIONS = [
    "Assumption: the count is printed on stdout (no source, an assumption)",
    "The install command is in src/superclaude/cli/install_commands.py (read by the worker)",
    "Its tests live under tests/cli/ (read by the worker)",
]
REVERSED = contradiction_item(
    "reversed choice",
    '"keep the --depth flag"',
    "the draft renames it to --level (draft body, Fix approach)",
)
DROPPED = contradiction_item(
    "dropped requirement",
    '"print it as the last line"',
    "the draft never mentions the last line (draft body, Test plan)",
)
CHANGED = contradiction_item(
    "changed flag", "--mode bug", "the draft is filed as a feature (flags.md)"
)
FACT = contradiction_item(
    "user-stated fact contradicted by verified code",
    '"the helper is create_issue.py"',
    "the scripts folder of the skill holds no such file (folder listing)",
)


def _additions(count: int) -> list[str]:
    return [
        f"Assumption: extra fact {n} (no source, an assumption)" for n in range(count)
    ]


def test_empty_notes_ask_no_question():
    notes = build_notes([], [])
    assert read_notes(notes) == ([], [])
    assert questions_for(notes) == 0


def test_notes_where_none_is_the_only_item_equal_empty_notes():
    notes = build_notes(["None"], ["None"])
    assert notes == build_notes([], [])
    assert read_notes(notes) == ([], [])
    assert questions_for(notes) == 0


def test_additions_only_notes_ask_no_question_and_keep_every_addition():
    notes = build_notes(ADDITIONS, [])
    additions, contradictions = read_notes(notes)
    assert questions_for(notes) == 0
    assert additions == ADDITIONS
    assert contradictions == []
    assert any(item.startswith("Assumption:") for item in additions)


def test_contradiction_only_notes_ask_exactly_one_question():
    notes = build_notes([], [REVERSED])
    assert read_notes(notes) == ([], [REVERSED])
    assert questions_for(notes) == 1


def test_three_contradictions_share_one_question_that_can_name_all_three():
    three = [REVERSED, DROPPED, CHANGED]
    notes = build_notes([], three)
    _additions, contradictions = read_notes(notes)
    assert questions_for(notes) == 1
    assert contradictions == three


def test_mixed_notes_ask_one_question_and_keep_the_additions():
    notes = build_notes(ADDITIONS[:2], [REVERSED])
    additions, contradictions = read_notes(notes)
    assert questions_for(notes) == 1
    assert additions == ADDITIONS[:2]
    assert contradictions == [REVERSED]


@pytest.mark.parametrize("count", [0, 1, 5])
def test_the_number_of_additions_never_changes_the_question_count(count):
    assert questions_for(build_notes(_additions(count), [])) == 0
    assert questions_for(build_notes(_additions(count), [REVERSED])) == 1
    assert len(read_notes(build_notes(_additions(count), [REVERSED]))[0]) == count


# --- four categories, incomplete lines, preserved flag, secret material -------------

CATEGORY_ITEMS = dict(zip(CONFLICT_CATEGORIES, [REVERSED, DROPPED, CHANGED, FACT]))


@pytest.mark.parametrize("name", CONFLICT_CATEGORIES)
def test_each_of_the_four_categories_asks_exactly_one_question(name):
    item = CATEGORY_ITEMS[name]
    notes = build_notes([], [item])
    assert name in item
    assert read_notes(notes) == ([], [item])
    assert questions_for(notes) == 1


@pytest.mark.parametrize("name", CONFLICT_CATEGORIES)
def test_the_rule_and_the_template_name_each_category(name):
    assert name in prompt_rule_section(_text(CREATE_REF))
    assert name in _text(NOTES_TEMPLATE)


NO_WORDS = contradiction_item(
    "reversed choice", "", "the draft renames it to --level (draft body)"
)
NO_EVIDENCE = contradiction_item(
    "dropped requirement", '"print it as the last line"', ""
)
NO_CATEGORY = contradiction_item(
    "", '"keep the --depth flag"', "the draft renames it to --level (draft body)"
)


@pytest.mark.parametrize(
    "item",
    [NO_WORDS, NO_EVIDENCE, NO_CATEGORY],
    ids=["missing-user-words", "missing-evidence", "missing-category"],
)
def test_an_incomplete_contradiction_line_is_new_material_and_asks_nothing(item):
    notes = build_notes([], [item])
    assert read_notes(notes) == ([item.strip()], [])
    assert questions_for(notes) == 0


def test_an_incomplete_line_does_not_hide_a_complete_one():
    notes = build_notes([], [NO_WORDS, REVERSED])
    assert read_notes(notes) == ([NO_WORDS.strip()], [REVERSED])
    assert questions_for(notes) == 1


WAVE2_SENTENCE = "The issue is filed with the user's flags when the user gave them"
STEP7_START = "7. Standard or deep with all flags given"
FLAG_DISAGREEMENT = (
    "Flag note: the worker would choose --mode feature; the issue is filed with the"
    " user's --mode bug (flags.md)"
)
FLAG_CHANGED = contradiction_item(
    "changed flag",
    "--mode bug",
    "the drafted issue uses --mode feature (draft title prefix [FEATURE])",
)


def flag_preservation_problems(ref: str) -> list[str]:
    """Problems with the preserved-flag sentence and the pushback comment step."""
    wave2 = ref[ref.index("## Wave 2") : ref.index("\n## Wave 3")]
    step7 = next((ln for ln in ref.splitlines() if ln.startswith(STEP7_START)), "")
    problems = []
    if WAVE2_SENTENCE not in wave2:
        problems.append("the Wave 2 section lacks the user's-flags sentence")
    if "gh issue comment" not in step7:
        problems.append("Wave 5 step 7 no longer posts the pushback comment")
    return problems


def test_a_worker_disagreement_recorded_as_new_material_asks_no_question():
    notes = build_notes([FLAG_DISAGREEMENT], [])
    assert "--mode bug" in FLAG_DISAGREEMENT
    assert read_notes(notes) == ([FLAG_DISAGREEMENT], [])
    assert questions_for(notes) == 0


def test_a_changed_flag_contradiction_with_the_flag_as_passed_asks_one_question():
    notes = build_notes([], [FLAG_CHANGED])
    assert read_notes(notes) == ([], [FLAG_CHANGED])
    assert questions_for(notes) == 1


def test_the_shipped_rule_files_with_the_user_flag_and_keeps_the_pushback_comment():
    assert flag_preservation_problems(_text(CREATE_REF)) == []


def test_flag_check_fails_when_only_the_wave_2_sentence_is_removed():
    ref = _text(CREATE_REF)
    wave2 = ref[ref.index("## Wave 2") : ref.index("\n## Wave 3")]
    assert WAVE2_SENTENCE in prompt_rule_section(ref)  # the copy the check ignores
    cut = ref.replace(wave2, wave2.replace(WAVE2_SENTENCE, "removed"))
    assert WAVE2_SENTENCE in prompt_rule_section(cut)
    assert flag_preservation_problems(cut) == [
        "the Wave 2 section lacks the user's-flags sentence"
    ]


def test_flag_check_fails_when_the_wave_5_pushback_is_removed():
    ref = _text(CREATE_REF)
    step7 = next(ln for ln in ref.splitlines() if ln.startswith(STEP7_START))
    cut = ref.replace(step7, step7.replace("gh issue comment", "gh issue note"))
    assert flag_preservation_problems(cut) == [
        "Wave 5 step 7 no longer posts the pushback comment"
    ]


SECRET_PLACE = "the place, never the value"
SECRET_ASKED = "so the contradiction question is asked"
SECRET_ITEM = contradiction_item(
    SECRET_CATEGORY, "n/a", "place: the Fix approach section of the draft body"
)


def secret_exception_problems(ref: str, template: str) -> list[str]:
    """Problems with the secret-material exception in the rule and the template."""
    problems = []
    for where, text in (("refs/create.md", ref), ("draft-notes template", template)):
        for needle in (SECRET_PLACE, SECRET_ASKED):
            if needle not in text:
                problems.append(f"{where} lacks {needle!r}")
    return problems


def test_a_secret_place_item_asks_one_question_without_quoted_user_words():
    notes = build_notes([], [SECRET_ITEM])
    assert QUOTED_WORDS.search(SECRET_ITEM) is None
    assert re.search(r"[A-Za-z0-9+/=_-]{24,}", SECRET_ITEM) is None  # no value in it
    assert read_notes(notes) == ([], [SECRET_ITEM])
    assert questions_for(notes) == 1


def test_both_shipped_files_carry_the_secret_material_exception():
    problems = secret_exception_problems(_text(CREATE_REF), _text(NOTES_TEMPLATE))
    assert problems == []


@pytest.mark.parametrize("needle", [SECRET_PLACE, SECRET_ASKED])
@pytest.mark.parametrize("where", ["refs/create.md", "draft-notes template"])
def test_secret_exception_check_fails_when_a_file_loses_the_exception(where, needle):
    ref, template = _text(CREATE_REF), _text(NOTES_TEMPLATE)
    if where == "refs/create.md":
        ref = ref.replace(needle, "removed")
    else:
        template = template.replace(needle, "removed")
    assert secret_exception_problems(ref, template) == [f"{where} lacks {needle!r}"]
