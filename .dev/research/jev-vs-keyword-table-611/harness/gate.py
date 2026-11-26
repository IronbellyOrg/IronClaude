"""The manifest and the two gates that keep every live call closed.

Command line (each takes ``--root``, the experiment folder by default):
  gate.py freeze-corpus   screen and freeze the corpus, its two records, ``questions.py`` and the model pin
  gate.py gate1           check the rule file and the corpus-side hashes; accepts UNSET values
  gate.py freeze-table    freeze the table answers and their provenance (after Gate 1 passes)
  gate.py freeze-rule     freeze the rule file's hash (refuses any UNSET value)
  gate.py record-tests    run the harness tests and record the result with the hash of every code file
  gate.py gate2           everything Gate 1 checks, plus the rest; a pass is what the live run rests on (a lead_go that names the
                          current rule hash must already be recorded, or it fails)
Only the three ``freeze-*`` commands write the manifest, each its own keys and never an existing key.  The gates only read it, and
they hash files only: they never call the corpus loader.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

_EXP = pathlib.Path(__file__).resolve().parents[1]
_JEV = _EXP.parent / "346-review-loop-experiments" / "p15" / "jev"
for _p in (str(_EXP), str(_JEV)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from harness import events, loader, spend  # noqa: E402

REPO = loader.EXPERIMENT.parents[2]
# manifest key -> the Paths attribute of the file it hashes (the corpus side, frozen by freeze-corpus)
CORPUS_SIDE = {"corpus": "corpus", "selection_criteria": "selection_criteria", "labelling_record": "labelling_record",
               "questions": "questions_py"}


class GateError(Exception):
    """A freeze or a recording step was refused."""


def read_manifest(paths):
    if not paths.manifest.is_file():
        return {}
    try:
        return json.loads(paths.manifest.read_text(encoding="utf-8"))
    except ValueError:
        raise GateError("manifest.json is not valid JSON") from None


def _write_manifest_keys(paths, new):
    m = read_manifest(paths)
    held = sorted(k for k in new if k in m)
    if held:
        raise GateError("the manifest already holds " + ", ".join(held) + "; a frozen value is never replaced")
    m.update(new)
    tmp = paths.manifest.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(m, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, paths.manifest)


def _code_hashes(paths):
    """SHA-256 of every code file of the experiment and every top-level jevlib file, by a stable name."""
    h = {}
    for p in paths.code_files():
        if p.is_file():
            h["code/" + p.relative_to(paths.root).as_posix()] = loader.sha256_file(p)
    for p in paths.jevlib_files():
        h["jevlib/" + p.name] = loader.sha256_file(p)
    return h


def _remaining_tokens(paths, cap_tokens):
    """Tokens still free under the cap: the ledger read as plain JSON (never through Budget, which rewrites it)."""
    if not paths.ledger.is_file():
        return cap_tokens
    led = json.loads(paths.ledger.read_text(encoding="utf-8"))
    pending = sum(d["est"] for d in led.get("draws", {}).values() if d.get("actual") is None)
    undrawn = sum(max(r["tokens"] - r["drawn"], 0) for r in led.get("reserved", {}).values())
    committed = led.get("spent_tokens", 0) + pending + undrawn
    return min(led.get("ceiling_input_tokens", cap_tokens), cap_tokens) - committed


def _spend_bound_reason(paths, price):
    """Why the whole-run worst case does not fit, or ``None``.  The prompts are read as JSON lines, not through the loader."""
    try:
        rule = loader.load_rule(paths.rule)
        rows = [json.loads(line) for line in paths.corpus.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (loader.LoadError, OSError, ValueError):
        return "the rule file or the corpus cannot be read"
    import questions
    from jevlib.questions import build_request
    qs = questions.build_questions()
    est = spend.estimate_run_tokens([build_request({"prompt": r["text"]}, qs) for r in rows])
    cap = rule["spend_cap_usd"]
    if spend.worst_case_usd(est, price) > cap:
        return "the whole-run worst case costs more than the cap"
    if est > _remaining_tokens(paths, spend.ceiling_tokens(cap, price)):
        return "the whole-run estimate is above the allowance left in the ledger"
    return None


def _gate1_checks(paths):
    failed = []
    if not paths.rule.is_file():
        failed.append("rule_missing")
    else:
        try:
            loader.load_rule(paths.rule)
        except loader.LoadError as e:
            msg = str(e)
            if "not AGREED" in msg:
                failed.append("rule_status")
            elif "is empty" in msg or "agreement text" in msg:
                failed.append("rule_provenance_empty")
            else:
                failed.append("rule_invalid")
    m = read_manifest(paths)
    if any(k not in m for k in CORPUS_SIDE):
        failed.append("manifest_missing")
    else:
        for key, attr in CORPUS_SIDE.items():
            p = getattr(paths, attr)
            if not p.is_file() or loader.sha256_file(p) != m[key]:
                failed.append("hash_" + key)
    return failed


def _gate2_checks(paths):
    failed = _gate1_checks(paths)
    m = read_manifest(paths)
    rule_sha = loader.sha256_file(paths.rule) if paths.rule.is_file() else None
    try:
        loader.load_rule(paths.rule, for_scoring=True)
    except loader.LoadError as e:
        if "UNSET" in str(e):
            failed.append("unset_value")
    if events.latest(paths, "rule_freeze") is None or "rule" not in m:
        failed.append("rule_not_frozen")
    if "rule" in m and m["rule"] != rule_sha:
        failed.append("hash_rule")
    for key, missing, mismatch in (("table_answers", "table_missing", "hash_table_answers"),
                                   ("table_provenance", "table_provenance_missing", "hash_table_provenance")):
        p = getattr(paths, key)
        if not p.is_file():
            failed.append(missing)
        elif m.get(key) != loader.sha256_file(p):
            failed.append(mismatch)
    tests = events.latest(paths, "tests_passed")
    if tests is None:
        failed.append("tests_not_recorded")
    elif tests.get("code_hashes") != _code_hashes(paths):
        failed.append("hash_code")
    price = events.latest(paths, "price_confirmed")
    if price is None:
        failed.append("price_not_confirmed")
    elif _spend_bound_reason(paths, price["usd_per_mtok"]):
        failed.append("spend_bound")
    go = events.latest(paths, "lead_go")
    if go is None:
        failed.append("go_missing")
    elif go.get("rule_sha256") != rule_sha:
        failed.append("go_rule_hash")
    if events.latest(paths, "first_request") or events.latest(paths, "run_end"):
        failed.append("prior_run")
    return failed


def gate1(paths):
    """Run Gate 1, write its result as an event and return the failed checks by name (an empty list is a pass)."""
    failed = _gate1_checks(paths)
    events.append_event(paths, "gate1", passed=not failed, failed=failed)
    return failed


def gate2(paths):
    """Run Gate 2, write its result as an event and return the failed checks by name (an empty list is a pass)."""
    failed = _gate2_checks(paths)
    events.append_event(paths, "gate2", passed=not failed, failed=failed)
    return failed


def freeze_corpus(paths):
    rows = loader.load_corpus(paths.corpus)
    for p in (paths.selection_criteria, paths.labelling_record, paths.questions_py):
        if not p.is_file():
            raise GateError(f"{p.name} is missing")
    from jevlib.config import MODEL
    keys = {k: loader.sha256_file(getattr(paths, attr)) for k, attr in CORPUS_SIDE.items()}
    keys["model_pin"] = MODEL
    _write_manifest_keys(paths, keys)
    events.append_event(paths, "freeze", evidence=paths.corpus, what="corpus", prompts=len(rows))
    return keys


def freeze_table(paths):
    failed = _gate1_checks(paths)
    if failed:
        raise GateError("Gate 1 checks fail: " + ", ".join(failed))
    for p in (paths.table_answers, paths.table_provenance):
        if not p.is_file():
            raise GateError(f"{p.name} is missing")
    keys = {"table_answers": loader.sha256_file(paths.table_answers),
            "table_provenance": loader.sha256_file(paths.table_provenance)}
    _write_manifest_keys(paths, keys)
    events.append_event(paths, "freeze", evidence=paths.table_answers, what="table")
    return keys


def freeze_rule(paths):
    loader.load_rule(paths.rule, for_scoring=True)
    keys = {"rule": loader.sha256_file(paths.rule)}
    _write_manifest_keys(paths, keys)
    events.append_event(paths, "rule_freeze", evidence=paths.rule)
    return keys


def _run(cmd):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return r.returncode, r.stdout + r.stderr


def _tests_command(paths):
    """``uv run pytest <tests folder> -v``, the folder relative to the repository root when it is under it."""
    try:
        folder = paths.tests_dir.relative_to(REPO).as_posix()
    except ValueError:
        folder = str(paths.tests_dir)
    return ["uv", "run", "pytest", folder, "-v"]


def record_tests(paths, runner=None):
    """Run the harness tests (``runner`` is injected in tests) and record the result with the hash of every code file."""
    cmd = _tests_command(paths)
    code, out = (runner or _run)(cmd)
    if code != 0:
        raise GateError("the test run failed")
    m = re.search(r"(\d+) passed", out)
    count = int(m.group(1)) if m else 0
    if count == 0:
        raise GateError("the test run passed no tests")
    return events.append_event(paths, "tests_passed", command=" ".join(cmd), count=count, code_hashes=_code_hashes(paths))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="gate.py", description="freeze the experiment's inputs and check the two gates")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("freeze-corpus", "gate1", "freeze-table", "freeze-rule", "record-tests", "gate2"):
        sub.add_parser(name).add_argument("--root", default=None)
    args = ap.parse_args(argv)
    paths = loader.Paths(args.root)
    try:
        if args.cmd in ("gate1", "gate2"):
            failed = (gate1 if args.cmd == "gate1" else gate2)(paths)
            print("PASS" if not failed else "FAILED: " + ",".join(failed))
            return 1 if failed else 0
        result = {"freeze-corpus": freeze_corpus, "freeze-table": freeze_table, "freeze-rule": freeze_rule,
                  "record-tests": record_tests}[args.cmd](paths)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (GateError, loader.LoadError) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
