"""E3 question set: the ONLY file with question wording (contract J7).  Changing any wording bumps QSET_VERSION.

Report Choices (relation {conflict, compatible, insufficient}; consequence {supported, refuted, insufficient}) are realized as
Nouls plus the companion Noul `evidence_sufficient` for the null case.  `refuted` has no action: Jev cannot reject, a low
`outcome_follows` only routes the finding to the conventional verifier."""
import e3lib  # noqa: F401  (puts jevlib on sys.path)
from jevlib.questions import noul

QSET_VERSION = "e3-q1"

OUTCOME_FOLLOWS = noul(
    "Does an implementer who follows the texts in `evidence` as written build the outcome described in `finding.wrong_outcome`?",
    "Read as written, the texts in `evidence` lead an implementer to the outcome in `finding.wrong_outcome`.",
    "Read as written, the texts in `evidence` lead an implementer to a different outcome from the one in `finding.wrong_outcome`.")

TEXTS_CONFLICT = noul(
    "Do `evidence.e1.text` and `evidence.e2.text` require incompatible outcomes for the same situation?",
    "No implementation can satisfy `evidence.e1.text` and `evidence.e2.text` in the same situation.",
    "One implementation can satisfy both `evidence.e1.text` and `evidence.e2.text`, for example because they apply to different conditions.")

EVIDENCE_SUFFICIENT = noul(
    "Do the texts in `evidence` contain everything needed to judge whether the outcome in `finding.wrong_outcome` follows, without other parts of the document?",
    "The quoted texts and their surrounding lines in `evidence` are enough to judge the claimed outcome.",
    "Judging the claimed outcome needs a part of the document that `evidence` does not include, such as a definition or an exception stated elsewhere.")

QUESTION_NAMES = ("outcome_follows", "texts_conflict", "evidence_sufficient")


def build_questions(state: dict) -> dict:
    """The question dict for one state: `texts_conflict` only when exactly two evidence texts exist."""
    qs = {"outcome_follows": OUTCOME_FOLLOWS}
    if state["facts"]["evidence_count"] == 2:
        qs["texts_conflict"] = TEXTS_CONFLICT
    qs["evidence_sufficient"] = EVIDENCE_SUFFICIENT
    return qs
