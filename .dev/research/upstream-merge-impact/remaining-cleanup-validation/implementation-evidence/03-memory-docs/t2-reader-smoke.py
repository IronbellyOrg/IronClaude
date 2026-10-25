# Task 2 behavioral smoke check (SEPARATE from the static check). Exercises the existing ReflexionPattern
# against ISOLATED storage rooted under this evidence folder; production memory/mistakes paths are never used.
import json, shutil, sys
from pathlib import Path

EVID = Path(".dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/03-memory-docs").resolve()
root = EVID / "t2-isolated"
assert root.resolve().parent == EVID, "isolated root must sit directly under the evidence folder"
shutil.rmtree(root, ignore_errors=True)
mem = root / "docs" / "memory"          # sibling mistakes dir becomes root/docs/mistakes (reflexion.py:78)
mem.mkdir(parents=True)
shutil.copy("docs/memory/reflexion.jsonl.example", mem / "solutions_learned.jsonl")

from superclaude import ReflexionPattern
r = ReflexionPattern(memory_dir=mem)
assert r.memory_dir == mem and r.mistakes_dir == root / "docs" / "mistakes"
rows = [json.loads(l) for l in open(mem / "solutions_learned.jsonl")]
row1 = rows[0]
tests = [
    ("0.90 pair", {"error_type": "ValueError", "error_message": "invalid port value 9090 in config file", "test_name": "test_load_config"}, True),
    ("0.70 pair (inclusive boundary)", {"error_type": "ValueError", "error_message": "port value 9090 in settings", "test_name": "test_load_config"}, True),
    ("0.50 pair", {"error_type": "ValueError", "error_message": "invalid timeout value 30 in settings", "test_name": "test_load_settings"}, False),
    ("JWT message-only 4/8", {"error_message": "JWT token validation failed missing secret"}, False),
    ("KeyError row 2 own signature", {"error_type": "KeyError", "error_message": "missing key 'user_id' in session payload 7", "test_name": "test_session_lookup"}, True),
]
bad = 0
for name, cur, want in tests:
    got = r.get_solution(cur)
    ok = (got is not None) == want
    if want and name != "KeyError row 2 own signature":
        ok = ok and got["solution"] == row1["solution"] and got["root_cause"] == row1["root_cause"] and got["prevention"] == row1["prevention"]
    if name == "KeyError row 2 own signature" and got:
        ok = ok and got["solution"] == rows[1]["solution"]
    print(("PASS " if ok else "FAIL ") + name, "->", "match" if got else "no match")
    bad += not ok
st = r.get_statistics()
ok = st["total_errors"] == 6 and st["errors_with_solutions"] == 6
print(("PASS " if ok else "FAIL ") + f"get_statistics {st}"); bad += not ok
ok = (root / "docs" / "mistakes").is_dir() and not list((root / "docs" / "mistakes").iterdir())
print(("PASS " if ok else "FAIL ") + "sibling mistakes dir created inside isolated root and left empty (no record_error call)"); bad += not ok
print("RESULT:", "FAIL" if bad else "ALL PASS")
sys.exit(1 if bad else 0)
