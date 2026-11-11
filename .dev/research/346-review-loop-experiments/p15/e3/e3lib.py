"""Shared paths and small helpers for the E3 confirmation-screen falsifier (session 1).  Stdlib only; run with `uv run --no-project python`."""
import hashlib
import json
import os
import pathlib
import sys

sys.dont_write_bytecode = True

SP = pathlib.Path(os.environ.get("SP", "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad"))
JEV = pathlib.Path(os.environ.get("JEV", str(SP / "p15/jev")))
E3 = pathlib.Path(os.environ.get("E3", str(pathlib.Path(__file__).resolve().parent)))
CENTRAL = SP / "central"
for _p in (str(JEV), str(E3)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

S1_SPEC = SP / "exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
S1_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
OFF = E3 / "offline"
CASES = OFF / "cases"          # offline/cases/<split>/<case_id>.json   (J8)
POOL = OFF / "pool"            # offline/pool/<case_id>.json
LABELS = OFF / "labels"
WORKERS = OFF / "workers.json"
EXPERIMENT = "E3"


def sha_text(t):
    return hashlib.sha256(t.encode()).hexdigest()


def decision(path=None):
    import tomllib
    with open(path or (E3 / "decision.toml"), "rb") as f:
        return tomllib.load(f)


def thresholds(dec=None):
    t = (dec or decision())["thresholds"]
    return {"t_suff": float(t["t_suff"]), "t_follow": float(t["t_follow"]), "t_conflict": float(t["t_conflict"])}


_S1 = None


def s1_text():
    """The original S1 spec text; the sha256 is asserted."""
    global _S1
    if _S1 is None:
        b = S1_SPEC.read_bytes()
        assert hashlib.sha256(b).hexdigest() == S1_SHA, "S1 spec sha mismatch"
        _S1 = b.decode("utf-8")
    return _S1


def candidate_of(case):
    """Candidate document text of a case: inline `candidate_text` (synthetic) or the S1 spec."""
    pk = case["packet"]
    if "candidate_text" in pk:
        return pk["candidate_text"]
    return s1_text()


def read_jsonl(path):
    p = pathlib.Path(path)
    if not p.exists():
        return []
    out = []
    for ln in p.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def write_json(path, obj):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False))


def load_json(path, default=None):
    p = pathlib.Path(path)
    return json.loads(p.read_text()) if p.exists() else default


def load_cases(split=None):
    """All J8 case files under offline/cases[/split], sorted by case_id."""
    root = CASES / split if split else CASES
    out = []
    if root.exists():
        for p in sorted(root.rglob("*.json")):
            out.append(json.loads(p.read_text()))
    return sorted(out, key=lambda c: c["case_id"])
