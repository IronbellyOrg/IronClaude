"""Class cards as data (MR 3.0.3, DESIGN 4.1, 6.2, 13.2, DD-11).

One JSON file per class in cards/, checked against cards/schema.json. Everything that depends on the class list
(quotas, the printed question, the route, the promotion category, the arm K paragraph) reads it from here, so a
new class is one new card file and no code change (REQ-10).

The schema check is a small interpreter of the schema subset the schema uses (stdlib only, so the pre-pass needs
nothing else); tests cross-check it against the `jsonschema` package. `promote_category` is checked against the
real findings categories through scaffold/fnd.py (DESIGN 2.3), so a category added there needs no schema change.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CARDS_DIR = Path(__file__).resolve().parents[1] / "cards"

_TYPES = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
}


def _check(value, schema: dict, path: str, errors: list[str]) -> None:
    """Append one message to errors for every way value breaks schema (type, enum, pattern, sizes, members)."""
    want = schema.get("type")
    if want is not None:
        kinds = want if isinstance(want, list) else [want]
        if not any(_TYPES[k](value) for k in kinds):
            errors.append(f"{path}: expected {'/'.join(kinds)}")
            return
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: not one of {schema['enum']}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than {schema['minLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: does not match {schema['pattern']}")
    if _TYPES["integer"](value) and value < schema.get("minimum", value):
        errors.append(f"{path}: below {schema['minimum']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if schema.get("uniqueItems") and len({json.dumps(v) for v in value}) < len(
            value
        ):
            errors.append(f"{path}: items repeat")
        for i, item in enumerate(value):
            _check(item, schema.get("items", {}), f"{path}[{i}]", errors)
    if isinstance(value, dict):
        props = schema.get("properties", {})
        errors.extend(
            f"{path}: missing {k}" for k in schema.get("required", []) if k not in value
        )
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}: unknown field {k}" for k in value if k not in props)
        for k, sub in props.items():
            if k in value:
                _check(value[k], sub, f"{path}.{k}", errors)


def load_schema(directory: Path | str | None = None) -> dict:
    return json.loads(
        (Path(directory or CARDS_DIR) / "schema.json").read_text(encoding="utf-8")
    )


def validate(card: dict, schema: dict | None = None) -> list[str]:
    """Every problem found in one card, as strings; [] means valid. Checks the schema, then promote_category."""
    from scaffold import fnd  # the one coupling to the findings code (DESIGN 2.3)

    errors: list[str] = []
    _check(card, schema or load_schema(), "card", errors)
    cat = card.get("promote_category") if isinstance(card, dict) else None
    if isinstance(cat, str) and cat not in fnd.CATEGORIES:
        errors.append(f"card.promote_category: {cat!r} is not in FND.CATEGORIES")
    return errors


def load(directory: Path | str | None = None) -> dict[str, dict]:
    """{id: card} for every C<n>.json in directory (default cards/), in class order. Raises ValueError on a bad card.

    The folder's own schema.json is used. A file whose name differs from its `id` is an error.
    """
    root = Path(directory or CARDS_DIR)
    schema = load_schema(root)
    cards: dict[str, dict] = {}
    problems: list[str] = []
    for f in sorted(root.glob("C*.json")):
        card = json.loads(f.read_text(encoding="utf-8"))
        problems.extend(f"{f.name}: {e}" for e in validate(card, schema))
        if isinstance(card, dict) and card.get("id") != f.stem:
            problems.append(
                f"{f.name}: id {card.get('id')!r} differs from the file name"
            )
        if isinstance(card, dict) and isinstance(card.get("id"), str):
            cards[card["id"]] = card
    if problems:
        raise ValueError("; ".join(problems))
    return dict(sorted(cards.items(), key=lambda kv: int(kv[0][1:])))


def _field(name: str, cards: dict[str, dict] | None) -> dict[str, str]:
    return {i: c[name] for i, c in (cards if cards is not None else load()).items()}


def questions(cards: dict[str, dict] | None = None) -> dict[str, str]:
    """{class id: printed question}; only a card whose question holds «value» has a placeholder."""
    return _field("question_template", cards)


def routes(cards: dict[str, dict] | None = None) -> dict[str, str]:
    """{class id: `search` or `read`}."""
    return _field("route", cards)


def promote_category(card_id: str, cards: dict[str, dict] | None = None) -> str:
    """The findings category a promoted line of this class gets (DD-11)."""
    return _field("promote_category", cards)[card_id]


def definition(card_id: str, cards: dict[str, dict] | None = None) -> str:
    """The target-neutral definition of one class (the source of the arm K paragraph, DD-14)."""
    return _field("definition", cards)[card_id]
