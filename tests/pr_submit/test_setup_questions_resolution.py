"""FX3 regression backstop: SETUP_QUESTIONS deriver field-resolution AST test.

Locks the F3 correctness-bug class. The F3 root cause (see
``.dev/tasks/to-do/TASK-RF-qa-reflect-harden-20260703-044500/research/01-fx3-questions-resolution.md``):
``_evidence_attr`` reads the operator answer under ``answer_key = answer_attr or attr``
via a SILENT ``getattr(answers, answer_key, None)`` (questions.py:68,71). The buggy
original call was ``_evidence_attr("pr_number")`` with no ``answer_attr`` — ``answer_key``
resolved to ``"pr_number"``, which is NOT a ``SetupAnswers`` field, so the operator's
``probe_pr`` answer was silently dropped and the deriver always fell through to
``evidence.pr_number``. No exception, no warning. The fix (questions.py:136) passes
``answer_attr="probe_pr"``.

This test AST-introspects ``questions.py`` and asserts every deriver's string-literal
attribute reference resolves to a REAL field: answer-side literals ⊆
``dataclasses.fields(SetupAnswers)`` and evidence-side literals ⊆
``dataclasses.fields(EvidenceBundle)``. It is authored to PASS green against the current
(already-fixed) tree and to FAIL on any recurrence of the F3 class. The valid-name sets
are built DYNAMICALLY from the dataclasses (never hardcoded) so the test stays in sync,
and the direction is SUBSET (``referenced ⊆ valid``) so a real-but-unreferenced field like
``augment_app_slug`` (set via the ``detected_augment_identity`` flow, referenced by no
deriver) does not false-positive.
"""

from __future__ import annotations

import ast
import dataclasses

# Import the REAL surface directly from the concrete modules (NOT the package
# facade, which lazily resolves via __getattr__) so we can AST-parse the source
# file via its __file__ and read the concrete dataclasses.
from superclaude.pr_submit.contract_setup import evidence as evidence_mod
from superclaude.pr_submit.contract_setup import questions as questions_mod

_DERIVER_FACTORIES = frozenset({"_answer_default", "_evidence_attr"})


def _setup_answers_fields() -> frozenset[str]:
    """Valid answer-side names, built dynamically from the dataclass."""
    return frozenset(f.name for f in dataclasses.fields(questions_mod.SetupAnswers))


def _evidence_bundle_fields() -> frozenset[str]:
    """Valid evidence-side names, built dynamically from the dataclass."""
    return frozenset(f.name for f in dataclasses.fields(evidence_mod.EvidenceBundle))


def _parse_questions_ast() -> ast.Module:
    """Parse questions.py from its real source file on disk."""
    source = open(questions_mod.__file__, encoding="utf-8").read()
    return ast.parse(source, filename=questions_mod.__file__)


def _deriver_calls(tree: ast.Module) -> list[ast.Call]:
    """Every ast.Call whose func is a bare Name of a deriver factory."""
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in _DERIVER_FACTORIES
    ]


def _const_str(node: ast.expr | None) -> str | None:
    """Return the str value if node is an ast.Constant str, else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _answer_default_literals(calls: list[ast.Call]) -> list[tuple[int, ast.expr]]:
    """(lineno, arg-node) for the single positional arg of each _answer_default."""
    out: list[tuple[int, ast.expr]] = []
    for call in calls:
        if isinstance(call.func, ast.Name) and call.func.id == "_answer_default":
            assert call.args, (
                f"_answer_default at line {call.lineno} has no positional arg; "
                "a deriver factory call must name an answer field literal."
            )
            out.append((call.lineno, call.args[0]))
    return out


def _evidence_attr_pairs(
    calls: list[ast.Call],
) -> list[tuple[int, ast.expr, ast.expr | None]]:
    """(lineno, attr-node, answer_attr-node-or-None) for each _evidence_attr call.

    ``attr`` is the first positional arg (the evidence field). ``answer_attr`` is
    the keyword ``answer_attr`` if present, else the second positional arg if given,
    else None (in which case answer_key == attr).
    """
    out: list[tuple[int, ast.expr, ast.expr | None]] = []
    for call in calls:
        if isinstance(call.func, ast.Name) and call.func.id == "_evidence_attr":
            assert call.args, (
                f"_evidence_attr at line {call.lineno} has no positional arg; "
                "the evidence field name is required."
            )
            attr_node = call.args[0]
            answer_attr_node: ast.expr | None = None
            for kw in call.keywords:
                if kw.arg == "answer_attr":
                    answer_attr_node = kw.value
            if answer_attr_node is None and len(call.args) >= 2:
                answer_attr_node = call.args[1]
            out.append((call.lineno, attr_node, answer_attr_node))
    return out


def test_every_answer_default_literal_resolves_to_a_real_setupanswers_field() -> None:
    """FX3 assertion (1): _answer_default(<lit>) literals ⊆ SetupAnswers fields."""
    valid = _setup_answers_fields()
    calls = _deriver_calls(_parse_questions_ast())
    literals = _answer_default_literals(calls)
    assert literals, (
        "No _answer_default(...) calls were collected from questions.py; the AST "
        "scan is broken (the F3 backstop would be a silent no-op)."
    )
    for lineno, node in literals:
        name = _const_str(node)
        assert name is not None, (
            f"_answer_default at questions.py:{lineno} received a non-constant/"
            "non-str argument; a computed deriver arg would silently bypass this "
            "field-resolution check."
        )
        assert name in valid, (
            f'_answer_default("{name}") at questions.py:{lineno} references a '
            f"name that is not a SetupAnswers field {sorted(valid)}; a wrong "
            "literal here reads a nonexistent answer field (the F3 class)."
        )


def test_every_evidence_attr_answer_key_resolves_to_a_real_setupanswers_field() -> None:
    """FX3 assertion (2) — THE DIRECT F3 TRAP: _evidence_attr answer_key ⊆ SetupAnswers.

    The buggy original ``_evidence_attr("pr_number")`` derived answer_key="pr_number"
    (not a SetupAnswers field) and would fail here.
    """
    valid = _setup_answers_fields()
    calls = _deriver_calls(_parse_questions_ast())
    pairs = _evidence_attr_pairs(calls)
    assert pairs, (
        "No _evidence_attr(...) calls were collected from questions.py; the AST "
        "scan is broken (the direct F3 trap would be a silent no-op)."
    )
    for lineno, attr_node, answer_attr_node in pairs:
        attr = _const_str(attr_node)
        assert attr is not None, (
            f"_evidence_attr at questions.py:{lineno} received a non-constant/non-str "
            "positional attr; a computed arg would bypass the F3 check."
        )
        if answer_attr_node is None:
            answer_key = attr
        else:
            answer_key = _const_str(answer_attr_node)
            assert answer_key is not None, (
                f"_evidence_attr at questions.py:{lineno} received a non-constant/"
                "non-str answer_attr; a computed arg would bypass the F3 check."
            )
        assert answer_key in valid, (
            f"_evidence_attr at questions.py:{lineno} resolves answer_key="
            f'"{answer_key}", which is not a SetupAnswers field {sorted(valid)}. '
            "This is exactly the F3 bug: the operator answer is read under a "
            "nonexistent field via getattr(..., None) and silently dropped."
        )


def test_every_evidence_attr_evidence_side_resolves_to_a_real_evidencebundle_attr() -> (
    None
):
    """FX3 assertion (3): _evidence_attr positional attr ⊆ EvidenceBundle attrs."""
    valid = _evidence_bundle_fields()
    calls = _deriver_calls(_parse_questions_ast())
    pairs = _evidence_attr_pairs(calls)
    assert pairs, (
        "No _evidence_attr(...) calls collected; the evidence-side check is a no-op."
    )
    for lineno, attr_node, _answer_attr_node in pairs:
        attr = _const_str(attr_node)
        assert attr is not None, (
            f"_evidence_attr at questions.py:{lineno} received a non-constant/non-str "
            "positional attr; a computed arg would bypass the evidence-side check."
        )
        assert attr in valid, (
            f'_evidence_attr("{attr}", ...) at questions.py:{lineno} references an '
            f"evidence field not on EvidenceBundle {sorted(valid)}; the evidence "
            "fallback would silently read None."
        )


def test_every_collected_deriver_arg_is_a_string_constant() -> None:
    """FX3 assertion (4): every deriver factory arg node is an ast.Constant str.

    A future edit that passes a variable (e.g. ``_answer_default(some_var)``) would
    make the static field-resolution checks silently skip that call; this guard fails
    loudly instead so the F3 backstop cannot be bypassed by dynamic args.
    """
    calls = _deriver_calls(_parse_questions_ast())
    assert calls, (
        "No deriver factory calls collected; the Constant-arg guard is a no-op."
    )
    for call in calls:
        assert isinstance(call.func, ast.Name)
        factory = call.func.id
        for arg in call.args:
            assert _const_str(arg) is not None, (
                f"{factory} at questions.py:{call.lineno} has a non-constant/non-str "
                "positional argument; deriver field references must be string literals "
                "so FX3's static resolution check cannot be bypassed."
            )
        for kw in call.keywords:
            if kw.arg == "answer_attr":
                assert _const_str(kw.value) is not None, (
                    f"{factory} at questions.py:{call.lineno} has a non-constant/non-str "
                    "answer_attr keyword; it must be a string literal for FX3."
                )
