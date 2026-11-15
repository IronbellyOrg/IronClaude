"""The ember re-ask (DESIGN 7.6, DR-8, REQ-27): one repair call for a report that has no valid ledger-v1 block.

`reask_allowed(role_reask, ledger_missing, already_asked, now_s, b_s)` is the decision. It is pure: the clock is an
argument, nothing here reads a wall clock to decide. The constants 30 and 1.35 are read from config/values.json.

`repair_prompt(message)` is the wording of DESIGN 7.6 (REPAIR_HEAD, then BEGIN, the original message, END).
`command(model)` is the one fresh call under `timeout`; `run_reask` makes it through an injectable `run` callable
(`run(argv, stdin_text, cwd) -> (exit code, stdout, stderr)`; `default_run` starts the process), applies the
model-identity check of run-reviewer.sh and the acceptance rule of 7.6, and returns a record. `do_reask` is the folder
version the `reask` subcommand runs. A re-ask is recorded as `reask`, never as a retry; its seconds are `reask_s`.

Acceptance (`accept`): the repaired message replaces the original only if its ledger-v1 block parses directly above
the findings block (scaffold.ledgerv1.read through rl/ledger_api.py) and its findings block, parsed as JSON lines in
order, equals the original's. Rows of an accepted message are marked via_reask by the check (check --via-reask).
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import time
from pathlib import Path

from rl import ledger_api as api
from rl import lens as lens_mod
from scaffold import fnd

TOLERANCE = 1e-9
KILLED_EXITS = (124, 137)  # timeout: 124 on the term signal, 137 when it had to kill

# DESIGN 7.6, the quoted draft wording (tests/test_reask.py compares it with DESIGN.md)
REPAIR_HEAD = (
    "Your final message was kept as your review, but it has no valid `ledger-v1` block directly above the "
    "`## Findings block` heading, so the checks cannot read it. Your message follows between the lines marked BEGIN "
    "and END. Reply with the same message again, with one section added: the heading `## Ledger`, then one fenced "
    "block with info string `ledger-v1`, one JSON object per line with the keys item, verdict, quote_plan, "
    "quote_other, problem and ran, one line for each recipe row you actually ran. Do not add a row for a step you "
    "did not run. Do not change the findings block. Do not run any command."
)


def constants() -> tuple[int, float]:
    r = lens_mod.values()["reask"]
    return r["fixed_s"], r["factor"]


def reask_allowed(role_reask, ledger_missing, already_asked, now_s, b_s) -> bool:
    """True only for a role with `reask`, a reviewer with `ledger_missing`, no earlier re-ask, and a clock that leaves
    room: now_s + 30 <= 1.35 * b_s, equality counted (math.isclose, tolerance 1e-9)."""
    if not (role_reask and ledger_missing) or already_asked:
        return False
    fixed, factor = constants()
    end, limit = now_s + fixed, factor * b_s
    return end <= limit or math.isclose(end, limit, rel_tol=0, abs_tol=TOLERANCE)


def repair_prompt(message: str) -> str:
    return f"{REPAIR_HEAD}\nBEGIN\n{message.rstrip(chr(10))}\nEND\n"


def command(model: str, timeout_s: int | None = None) -> list[str]:
    """The argv of the fresh call (DESIGN 7.6): the same flags as run-reviewer.sh, under `timeout 30`."""
    return [
        "timeout",
        str(timeout_s or constants()[0]),
        "claude",
        "-p",
        "--model",
        model,
        "--output-format",
        "json",
        "--no-session-persistence",
        "--permission-mode",
        "bypassPermissions",
        "--disallowedTools",
        "Edit",
        "Write",
        "NotebookEdit",
    ]


def default_run(argv, stdin_text, cwd):
    """Start the process (K2 and DD-8 hold: an allowed model and NOFALLBACK=1). Tests use the fake claude first on PATH."""
    if model_of(argv) not in lens_mod.allowed_models():
        raise ValueError(f"E_MODEL: {model_of(argv)} is not an allowed reviewer model")
    if os.environ.get("NOFALLBACK") != "1":
        raise RuntimeError("E_NOFALLBACK: NOFALLBACK=1 is required")
    p = subprocess.run(
        argv, input=stdin_text, capture_output=True, text=True, cwd=cwd, check=False
    )
    return p.returncode, p.stdout, p.stderr


def model_of(argv) -> str:
    return argv[argv.index("--model") + 1]


def parse_result(stdout: str) -> dict:
    """{message, observed_model, is_error, output_tokens_all} of the JSON array a `claude -p` run prints."""
    events = json.loads(stdout)
    results = [e for e in events if e.get("type") == "result"]
    observed = sorted(
        {
            e["message"]["model"]
            for e in events
            if e.get("type") == "assistant"
            and e.get("parent_tool_use_id") is None
            and e.get("message", {}).get("model")
        }
    )
    res = results[0] if results else {}
    tokens = sum(
        v.get("outputTokens", 0) for v in (res.get("modelUsage") or {}).values()
    )
    return {
        "message": res.get("result") or "",
        "observed_model": ",".join(observed),
        "is_error": bool(res.get("is_error")),
        "output_tokens_all": tokens,
    }


def model_ok(expected: str, observed: str) -> bool:
    """The identity check of run-reviewer.sh: the observed model is the requested one (or its -build name)."""
    obs, exp = observed.lower(), expected.lower()
    return bool(obs) and obs != "<synthetic>" and obs in (exp, f"{exp}-build")


def _findings_lines(report: str) -> list:
    """The findings block as JSON lines in order; a line that is not JSON stays as its text."""
    out = []
    for raw in fnd.lenient_lines(report):
        try:
            out.append(json.loads(raw))
        except json.JSONDecodeError:
            out.append(raw.strip())
    return out


def accept(original: str, repaired: str) -> tuple[bool, str]:
    """(accepted, reason) by the rule of DESIGN 7.6."""
    rd = api.read(repaired)
    if rd["ledger_missing"]:
        return False, f"ledger_missing:{rd['reason']}"
    if rd["block_unusable"] != api.read(original)["block_unusable"]:
        return False, "findings_block_unusable"
    if _findings_lines(repaired) != _findings_lines(original):
        return False, "findings_differ"
    return True, "accepted"


def run_reask(original, model, cwd, run=default_run, clock=time.monotonic) -> dict:
    """One repair call and its verdict. The record: asked, seconds, exit, killed, observed_model, model_ok,
    output_tokens_all, accepted, reason and (when accepted) message. It never raises for a failed call."""
    argv = command(model)
    rec = {
        "asked": True,
        "seconds": 0.0,
        "exit": None,
        "killed": False,
        "observed_model": "",
        "model_ok": False,
        "output_tokens_all": 0,
        "accepted": False,
        "reason": None,
    }
    start = clock()
    try:
        rc, out, _err = run(argv, repair_prompt(original), cwd)
    except Exception as e:  # claude missing, a refused model: the original report stays
        rec.update(
            seconds=round(clock() - start, 3), reason=f"error:{type(e).__name__}"
        )
        return rec
    rec.update(seconds=round(clock() - start, 3), exit=rc, killed=rc in KILLED_EXITS)
    if rec["killed"]:
        rec["reason"] = "killed"
        return rec
    try:
        res = parse_result(out)
    except (ValueError, AttributeError, TypeError):
        rec["reason"] = "no_result"
        return rec
    rec.update(
        observed_model=res["observed_model"],
        model_ok=model_ok(model, res["observed_model"]),
        output_tokens_all=res["output_tokens_all"],
    )
    if rc != 0 or res["is_error"] or "API Error" in res["message"]:
        rec["reason"] = "call_failed"
    elif not res["message"].strip():
        rec["reason"] = "no_result"
    elif not rec["model_ok"]:
        rec["reason"] = "wrong_model"
    else:
        rec["accepted"], rec["reason"] = accept(original, res["message"])
        if rec["accepted"]:
            rec["message"] = res["message"]
    return rec


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def do_reask(
    run_dir, rid, cwd, now_s, b_s=None, run=default_run, clock=time.monotonic
) -> dict:
    """The re-ask of one reviewer of a run folder (R3). Reads lens/<rid>.json and reviews/<rid>.md; always writes
    reviews/<rid>.reask.json (allowed, reason, accepted, seconds, ...). When the call ran and was accepted, the
    original goes to reviews/<rid>.preask.md and the repaired message to reviews/<rid>.reask.md and reviews/<rid>.md,
    so the check that follows reads it (with --via-reask <rid>). Otherwise reviews/<rid>.md is not touched."""
    reviews = Path(run_dir) / "reviews"
    lens = json.loads(
        (Path(run_dir) / "lens" / f"{rid}.json").read_text(encoding="utf-8")
    )
    original = (reviews / f"{rid}.md").read_text(encoding="utf-8")
    record_path = reviews / f"{rid}.reask.json"
    prior = (
        json.loads(record_path.read_text(encoding="utf-8"))
        if record_path.is_file()
        else {}
    )
    b_s = lens["b"] if b_s is None else b_s
    missing = api.read(original)["ledger_missing"]
    ok = reask_allowed(lens["reask"], missing, bool(prior.get("asked")), now_s, b_s)
    if ok:
        rec = run_reask(original, lens["model"], cwd, run, clock)
    else:
        why = (
            "role_not_reasked"
            if not lens["reask"]
            else "ledger_present"
            if not missing
            else "already_asked"
            if prior.get("asked")
            else "too_late"
        )
        rec = {
            "asked": bool(prior.get("asked")),
            "accepted": False,
            "reason": why,
            "seconds": 0.0,
        }
    message = rec.pop("message", None)
    rec.update(rid=rid, allowed=ok, now_s=now_s, b_s=b_s)
    if message is not None:
        _write(reviews / f"{rid}.preask.md", original)
        _write(reviews / f"{rid}.reask.md", message)
        _write(reviews / f"{rid}.md", message)
    if ok or not prior.get(
        "asked"
    ):  # the record of the call that ran is never overwritten
        _write(
            record_path,
            json.dumps(rec, sort_keys=True, ensure_ascii=False, indent=1) + "\n",
        )
    return rec
