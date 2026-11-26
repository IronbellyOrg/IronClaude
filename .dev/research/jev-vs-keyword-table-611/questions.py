"""The only place Jev question wording for the issue 611 experiment lives (contract J7).

Two questions are asked about the prompt in ``state["prompt"]``: which of six problem types it is (a Choice), and whether any of
the six fits at all (a Noul).  The six definitions are written in plain words; they are not a copy of the keyword table the
experiment compares against, and no corpus prompt, label or example appears here.
"""
from jevlib.questions import choice, noul

QSET_VERSION = "issue611-q1"
TYPES = ("bug", "build", "performance", "deployment", "security", "test")

_DEFINITIONS = {
    "bug": "The program gives a wrong result or stops with an error because of a mistake in its own code.",
    "build": "The steps that assemble the project, or check it before it runs, stop with an error.",
    "performance": "The program works but uses too much time or memory for what it does.",
    "deployment": "The program works where it was built but fails when it is installed, configured or started on the machine meant to run it.",
    "security": "Someone could misuse the program to read or change data they should not, or to take control of something.",
    "test": "The automated checks of the program fail, pass only some of the time, or do not check what they claim to check.",
}


def build_questions() -> dict:
    """Return the two questions in a fixed order; the request hash is stable across calls."""
    return {
        "problem_type": choice(
            "Read the problem described in the prompt field of the state and pick the one type that describes it best.",
            {t: _DEFINITIONS[t] for t in TYPES},
        ),
        "any_type_fits": noul(
            "Read the problem described in the prompt field of the state. Decide whether any of the six problem types "
            "(bug, build, performance, deployment, security, test) describes it.",
            true="At least one of the six problem types describes the problem.",
            false="None of the six problem types describes the problem.",
        ),
    }
