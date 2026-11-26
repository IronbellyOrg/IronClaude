"""Drift guard for the plain-English bullets and the fixed wrap-up body in pragmatic.md.

Pure file-content assertions on `src/superclaude/output-styles/pragmatic.md`: the four
plain-English conventions added after the self-sufficient-message rule, and the five bold
headings of the wrap-up template, in order. No HOME file, no network, no subprocess.
"""

from pathlib import Path

_STYLE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "output-styles"
    / "pragmatic.md"
)

_PLAIN_ENGLISH_BULLETS = [
    "- Use the names that the user and the product use, not our own internal names "
    "for things, and describe each thing in plain words.",
    "- Write every named thing as its name followed by what it is in a few plain "
    "words, with its link or path, the first time it appears.",
    "- Follow every question or approval request with one line per possible answer "
    "saying what that answer would do.",
    "- Before sending, check four things:",
]

_QUESTION_CONTEXT = (
    "- Before every question or decision request (including approval), assume the user "
    "is coming in blind, with none of the session's context. Give the context, "
    "implications and risks in roughly one line each before asking; this is necessary "
    "context, not filler. Link an existing file with more detail when available. "
    "Never create a file just to link it. If no existing file has the detail, say so plainly."
)

_DECISION_BULLETS = [
    "- Never ask what can be self-answered. Three-way gate before surfacing anything: "
    "(a) answer findable in the artifacts/code/own capability: resolve it and report, "
    "never ask; (b) genuinely the user's decision (taste, scope, priorities, destructive "
    "or outward actions): ask EXACTLY ONE clear plain-English question with a "
    "recommendation; (c) neither (speculative, non-actionable): do not raise it.",
    '- No hedging: no half-formed "one nuance worth flagging" offers that are neither '
    "a committed action nor a clear question.",
    "- Present decisions ONE at a time, never as a batched table of terms. Each option "
    "must be self-sufficient: define the term, state concretely what each value would "
    "DO and why it matters, give an example, and include a recommendation.",
    '- Never manufacture a multi-option "design decision" out of a defect-to-fix. '
    "State the defect plainly in one sentence with the one concrete example first.",
]

_WRAP_UP_HEADINGS = [
    "**What I did**",
    "**How**",
    "**Where it stands**",
    "**What's next**",
    "**My recommendation**",
]


def _text() -> str:
    return _STYLE.read_text(encoding="utf-8")


def _in_order(text: str, needles: list[str]) -> bool:
    pos = -1
    for needle in needles:
        pos = text.find(needle, pos + 1)
        if pos < 0:
            return False
    return True


def test_four_plain_english_bullets_are_present_in_order():
    text = _text()
    for bullet in _PLAIN_ENGLISH_BULLETS:
        assert text.count(bullet) == 1, bullet
    assert _in_order(text, _PLAIN_ENGLISH_BULLETS)


def test_plain_english_bullets_sit_in_the_writing_conventions_section():
    text = _text()
    section = text.split("#### Plain English and writing conventions", 1)[1].split(
        "#### How and why questions", 1
    )[0]
    for bullet in _PLAIN_ENGLISH_BULLETS:
        assert bullet in section


def test_question_context_rule_is_unique_and_in_decision_requests():
    text = _text()
    section = text.split("#### Decision requests", 1)[1].split(
        "#### Status and wrap-ups", 1
    )[0]
    assert text.count(_QUESTION_CONTEXT) == 1
    assert _QUESTION_CONTEXT in section


def test_existing_question_rules_remain_in_source_order():
    text = _text()
    section = text.split("#### Decision requests", 1)[1].split(
        "#### Status and wrap-ups", 1
    )[0]
    for bullet in _DECISION_BULLETS:
        assert text.count(bullet) == 1, bullet
        assert bullet in section
    assert _in_order(
        text, [_PLAIN_ENGLISH_BULLETS[2], _QUESTION_CONTEXT, *_DECISION_BULLETS]
    )


def test_wrap_up_template_names_the_five_headings_in_order():
    text = _text()
    template = text.split("**Wrap-up** (completed work;", 1)[1].split(
        "**Multi-point reply**", 1
    )[0]
    assert _in_order(template, _WRAP_UP_HEADINGS)
    example = template.split("| NEXT |", 1)[1]
    labels = [f"{h[:-2]}:**" for h in _WRAP_UP_HEADINGS]
    assert _in_order(example, labels)
