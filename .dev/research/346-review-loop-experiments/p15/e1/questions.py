"""All E1/E4 question wording (contract J7: the only file with question text).  Plan section 2.2, exact wording."""
import _boot  # noqa: F401
from jevlib.questions import noul

QSET_VERSION = "e1-q1"
MAX_DEPS = 3

DEFECT_STILL_PRESENT = noul(
    "Does the text in `after.passage` still lead an implementer to the wrong outcome described in `defect.wrong_outcome`?",
    "Following `after.passage` as written still produces the outcome that `defect.wrong_outcome` calls wrong.",
    "Following `after.passage` as written produces a different outcome from the one `defect.wrong_outcome` calls wrong.")

OBLIGATION_STILL_REQUIRED = noul(
    "Does the text in `after.passage` still require what `obligation.text` requires?",
    "`after.passage` states the requirement of `obligation.text`, in the same or in different words.",
    "`after.passage` no longer states the requirement of `obligation.text`: it was deleted, weakened or made optional.")

CONTEXT_SUFFICIENT = noul(
    "Does the state contain every passage needed to decide whether the requirement of `obligation.text` is still in force after the change?",
    "The passages in `after` and `dependencies` are enough to tell whether the requirement of `obligation.text` is still in force.",
    "Deciding needs a passage the state does not include, such as a section that `after.passage` refers to.")


def contradicts(k: int) -> dict:
    d = f"d{k}"
    return noul(f"Does `after.passage` contradict `dependencies.{d}.text`?",
                f"An implementer cannot follow both `after.passage` and `dependencies.{d}.text` in the same situation.",
                f"An implementer can follow both `after.passage` and `dependencies.{d}.text` together.")


def questions_for(n_deps: int) -> dict:
    """One request per packet: defect, obligation, one contradiction question per supplied dependency, and the companion."""
    if not 0 <= n_deps <= MAX_DEPS:
        raise ValueError(f"a packet carries 0..{MAX_DEPS} dependencies, got {n_deps}")
    q = {"defect_still_present": DEFECT_STILL_PRESENT, "obligation_still_required": OBLIGATION_STILL_REQUIRED}
    for k in range(1, n_deps + 1):
        q[f"contradicts_d{k}"] = contradicts(k)
    q["context_sufficient"] = CONTEXT_SUFFICIENT
    return q


def question_names(n_deps: int) -> list:
    return list(questions_for(n_deps))


# ---------------------------------------------------------------- conventional checker brief (plan 2.4; E1 replay and the E4 CK worker)
CHECKER_BRIEF_TEXT = (
    "Evaluate only the supplied prior finding and mapped change. Distinguish removing the original defect from preserving the accepted obligation. "
    "Check supplied dependent passages. Reviewer/reviser assertions are not proof. Missing, conflicting or insufficient evidence means uncertainty "
    "for generative verification. Do not certify untouched global text.")


def checker_brief(packets_path, out_path) -> str:
    """Brief of the conventional checker: the report text verbatim, then the output contract.  The five judgments mirror the Jev questions."""
    return (
        f"{CHECKER_BRIEF_TEXT}\n\n"
        f"For each packet in {packets_path}, answer each question below with `yes`, `no` or `uncertain`, using only that packet: "
        "defect_still_present (does `after.passage` still lead an implementer to the wrong outcome in `defect.wrong_outcome`?), "
        "obligation_still_required (does `after.passage` still require what `obligation.text` requires?), "
        "contradicts_dK for each supplied dependency dK (does `after.passage` contradict it?), "
        "context_sufficient (do the supplied passages suffice to decide whether the requirement of `obligation.text` is still in force?). "
        f"Write one JSON line per packet to {out_path}: "
        '{"packet_id": "...", "defect_still_present": "...", "obligation_still_required": "...", "contradicts_d1": "...", '
        '"context_sufficient": "...", "quote": "<the after text you relied on>"}. '
        "Add one contradicts_dK key per dependency the packet supplies and none for a packet without dependencies. Edit nothing else.")
