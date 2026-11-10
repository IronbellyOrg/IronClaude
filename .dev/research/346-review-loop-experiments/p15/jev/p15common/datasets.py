"""Offline datasets (contract J8): group-level splits, case files, label packets."""
import hashlib
import json
import pathlib

CASE_KEYS = ["case_id", "group", "family", "category", "variant", "split", "data_classes", "source", "packet", "author_intent"]
SOURCE_KINDS = {"synthetic", "public", "s1", "stage2"}


def split_groups(groups, seed, sizes) -> dict:
    """group -> split.  Deterministic, stable under input order.  `sizes` maps split name to a count (int) or a fraction (float <= 1);
    groups left over after the listed sizes go to the last split name."""
    uniq = sorted(set(groups), key=lambda g: (hashlib.sha256(f"{seed}:{g}".encode()).hexdigest(), g))
    n = len(uniq)
    names = list(sizes)
    counts = {}
    for nm in names:
        v = sizes[nm]
        counts[nm] = int(round(v * n)) if isinstance(v, float) and v <= 1.0 else int(v)
    if sum(counts.values()) > n:
        raise ValueError(f"split sizes {counts} exceed the {n} groups")
    counts[names[-1]] += n - sum(counts.values())
    out, i = {}, 0
    for nm in names:
        for g in uniq[i:i + counts[nm]]:
            out[g] = nm
        i += counts[nm]
    return out


def _has_key(obj, key):
    if isinstance(obj, dict):
        return key in obj or any(_has_key(v, key) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_key(v, key) for v in obj)
    return False


def validate_case(case: dict) -> None:
    missing = [k for k in CASE_KEYS if k not in case]
    if missing:
        raise ValueError(f"case missing keys {missing}")
    if not isinstance(case["packet"], dict) or _has_key(case["packet"], "author_intent"):
        raise ValueError("author_intent must never appear inside packet")
    if not isinstance(case["author_intent"], dict):
        raise ValueError("author_intent must be an object")
    src = case["source"]
    if not isinstance(src, dict) or src.get("kind") not in SOURCE_KINDS or "paths" not in src or "url" not in src:
        raise ValueError("source needs kind (synthetic|public|s1|stage2), paths and url")
    if not isinstance(case["data_classes"], list) or not case["data_classes"]:
        raise ValueError("data_classes must be a non-empty list")


def write_case(path, case: dict) -> None:
    validate_case(case)
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(case, indent=1, sort_keys=True))


def load_cases(dir) -> list:
    return [json.loads(p.read_text()) for p in sorted(pathlib.Path(dir).rglob("*.json"))]


def label_packet(case: dict, fields=None) -> dict:
    """What a labeler sees: the case id and the packet (optionally restricted to `fields`).  Never author_intent, split,
    group, family, category or variant metadata."""
    pk = case["packet"]
    if fields:
        pk = {k: pk[k] for k in fields if k in pk}
    return {"case_id": case["case_id"], "packet": json.loads(json.dumps(pk))}
