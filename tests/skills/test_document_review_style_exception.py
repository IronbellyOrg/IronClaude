"""Static precedence regression checks; not proof of live model compliance."""

from pathlib import Path

STYLE = (
    Path(__file__).resolve().parents[2] / "src/superclaude/output-styles/pragmatic.md"
)


def test_document_contract_exception_is_scoped_before_generic_rules():
    text = STYLE.read_text()
    start = text.index("#### Document-review contract exception")
    generic = text.index("- Every review agent MUST begin its review")
    assert start < generic
    section = text[start:generic]
    assert "For `/sc:spec-panel` document review in every mode only" in section
    assert "Other protocols, including implementation and PR-submit" in section
    assert "must not override this exception within it" in section


def test_document_exception_preserves_evidence_and_warning_policy():
    text = STYLE.read_text().split("#### Document-review contract exception", 1)[1]
    text = text.split("The generic rules below", 1)[0]
    for clause in (
        "An adequately evidenced zero-finding result is valid",
        "Genuine Medium/Low/Nit findings are warnings/notes",
        "Missing required evidence is INCOMPLETE",
        "no hidden fourth review or third fix",
        "No external issue is created without authorization",
    ):
        assert clause in text
