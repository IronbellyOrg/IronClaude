"""Developer tool (not shipped): build the four redacted message-read samples from recorded probes.

It makes NO Orca call. It reads the already recorded, sanitized probe outputs of the phase 2
gate research (``research/evidence/`` next to ``RESEARCH-REPORT-phase2-gate.md``, files 01, 03,
17 and 24) and writes four fixture files:

    golden-question-success.json  golden-question-missing.json
    golden-question-stale.json    golden-question-contradictory.json

    uv run python tests/observe/record_golden_questions.py --evidence <evidence dir>

Redaction (``redact_envelope``): message ids, Run ids and the Run inside a ``to_handle`` become
synthetic stable values; ``from_handle`` and ``body`` become ``redacted``; every key outside the
recorded set becomes ``redacted``; timestamps shift by one constant so the newest lands one
minute before the anchor; envelope and runtime ids become fixed placeholders. Key names and
value types are kept. Subjects are kept: they are the synthetic strings of the probes.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

from superclaude.cli.observe import adapter
from superclaude.cli.observe.parse import format_utc_iso, parse_timestamp

FIXTURES = Path(adapter.__file__).parent / "fixtures"
ANCHOR_TIME = 1794139200.0  # 2026-11-08T12:00:00Z (the observer tests' base time)
NEWEST_OFFSET = 60.0  # the newest recorded question lands one minute before the anchor

MESSAGE_KEYS = (
    "id",
    "run_id",
    "delivery_contract",
    "from_handle",
    "to_handle",
    "subject",
    "body",
    "type",
    "priority",
    "thread_id",
    "payload",
    "created_at",
    "delivered_at",
)
RUN_ID = re.compile(r"run_[0-9a-f]{12}")
EVIDENCE = {
    "success_b": "03-all-B.json",
    "success_a": "24-all-A-types-question.json",
    "fenced": "01-all-A-read1.json",
    "no_terminal": "17-unbound-all-A.json",
}


class Names:
    """Stable synthetic names: the nth distinct original gets the nth placeholder."""

    def __init__(self, fmt: str) -> None:
        self._fmt = fmt
        self._seen: dict[str, str] = {}

    def __call__(self, original: str) -> str:
        if original not in self._seen:
            self._seen[original] = self._fmt.format(n=len(self._seen) + 1)
        return self._seen[original]


def newest_created(envelopes: list[dict]) -> float:
    stamps = [
        parse_timestamp(m.get("created_at"))
        for env in envelopes
        for m in (env.get("result") or {}).get("messages") or []
        if isinstance(m, dict)
    ]
    return max(s for s in stamps if s is not None)


def redact_envelope(
    env: dict,
    *,
    envelope_id: str,
    runs: Names,
    messages: Names,
    shift: float,
) -> dict:
    """One redacted copy of a message-read envelope (success or error)."""
    if not isinstance(env, dict) or not isinstance(env.get("ok"), bool):
        raise ValueError("not a message-read envelope")
    out: dict = {"id": envelope_id, "ok": env["ok"]}
    if env["ok"]:
        result = env.get("result")
        if not isinstance(result, dict) or not isinstance(result.get("messages"), list):
            raise ValueError("result.messages is not a list")
        rows = [redact_message(m, runs, messages, shift) for m in result["messages"]]
        out["result"] = {
            "acknowledged": result.get("acknowledged"),
            "count": len(rows),
            "messages": rows,
            "runId": runs(result["runId"])
            if isinstance(result.get("runId"), str)
            else None,
        }
    else:
        error = env.get("error")
        if not isinstance(error, dict):
            raise ValueError("error is not an object")
        message = RUN_ID.sub(lambda m: runs(m.group(0)), str(error.get("message", "")))
        out["error"] = {"code": str(error.get("code", "")), "message": message}
    out["_meta"] = {"runtimeId": "redacted"}
    return out


def redact_message(raw: dict, runs: Names, messages: Names, shift: float) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("a message row is not an object")
    row: dict = {}
    for key in MESSAGE_KEYS:
        if key not in raw:
            continue
        value = raw[key]
        if key == "id":
            row[key] = f"msg_{int(messages(value)):012d}"
        elif key == "run_id":
            row[key] = runs(value)
        elif key == "to_handle":
            row[key] = (
                f"run:{runs(value.split(':', 1)[1])}"
                if value.startswith("run:")
                else "redacted"
            )
        elif key in ("from_handle", "body"):
            row[key] = "redacted"
        elif key == "payload":
            row[key] = None if value is None else "redacted"  # a null stays null
        elif key in ("created_at", "delivered_at"):
            epoch = parse_timestamp(value)
            row[key] = None if epoch is None else format_utc_iso(epoch + shift)
        else:
            row[key] = value
    for key in set(raw) - set(
        MESSAGE_KEYS
    ):  # keys outside the recorded set survive by name only
        row[key] = "redacted"
    return row


def load(evidence: Path) -> dict[str, dict]:
    return {
        name: json.loads((evidence / filename).read_text(encoding="utf-8"))
        for name, filename in EVIDENCE.items()
    }


def build(evidence: Path) -> dict[str, dict]:
    """The four fixture documents, keyed by variant name."""
    raw = load(evidence)
    shift = (
        ANCHOR_TIME
        - NEWEST_OFFSET
        - newest_created([raw["success_b"], raw["success_a"]])
    )
    runs = Names("run-{n}")  # run-1, run-2 ...
    messages = Names("{n}")  # the nth distinct original id becomes msg_<n>, zero padded
    # Run ids first, so the order is stable: the question Run of the probes is "run-a".
    letter = {"run_c1badaa6576b": "run-a", "run_14cfcbd8edf2": "run-b"}
    runs._seen.update(letter)

    def red(env: dict, label: str) -> dict:
        return redact_envelope(
            env, envelope_id=label, runs=runs, messages=messages, shift=shift
        )

    question_b = [
        m for m in raw["success_b"]["result"]["messages"] if m["type"] == "question"
    ]
    status_b = [
        m for m in raw["success_b"]["result"]["messages"] if m["type"] != "question"
    ]
    success = copy.deepcopy(raw["success_a"])
    success["result"]["messages"] = [
        *success["result"]["messages"],
        *[
            {
                **m,
                "run_id": success["result"]["runId"],
                "to_handle": f"run:{success['result']['runId']}",
            }
            for m in question_b
        ],
    ]
    success["result"]["messages"].sort(
        key=lambda m: m["created_at"], reverse=True
    )  # newest first
    success["result"]["count"] = len(success["result"]["messages"])
    good = red(success, "env-001")

    missing_cycle = red(raw["success_b"], "env-002")
    del missing_cycle["result"]["messages"]
    no_terminal = red(raw["no_terminal"], "env-003")

    contradictory_ok = copy.deepcopy(success)
    contradictory_ok["result"]["messages"] = [
        *contradictory_ok["result"]["messages"],
        *[
            {
                **m,
                "run_id": success["result"]["runId"],
                "to_handle": f"run:{success['result']['runId']}",
            }
            for m in status_b
        ],
        {
            **question_b[0],
            "id": "msg_zzzzzzzzzzzz",
            "run_id": raw["success_b"]["result"]["runId"],
        },
    ]
    contradictory_ok["result"]["count"] = len(contradictory_ok["result"]["messages"])
    contradictory = [red(contradictory_ok, "env-004"), red(raw["fenced"], "env-005")]

    return {
        "golden-question-success": {
            "variant": "golden-question-success",
            "description": "a good message read: two question rows of one Run, newest first",
            "cycles": [good],
        },
        "golden-question-missing": {
            "variant": "golden-question-missing",
            "description": "a good read, then an envelope without result.messages, then the no_active_terminal error",
            "cycles": [good, missing_cycle, no_terminal],
        },
        "golden-question-stale": {
            "variant": "golden-question-stale",
            "description": "the good read, then failing reads (the test moves the fake monotonic clock past 45 s)",
            "cycles": [
                good,
                {"fail": "timeout"},
                {"fail": "timeout"},
                {"fail": "timeout"},
            ],
        },
        "golden-question-contradictory": {
            "variant": "golden-question-contradictory",
            "description": "a good read, a read with a status row and a row of another Run, then the consumer_fenced error",
            "cycles": [good, *contradictory],
        },
    }


def build_cap(evidence: Path) -> dict:
    """The 100-row cap sample (evidence file 14: a 104-message probe Run read with ``--all``).

    Exactly 100 question rows, newest first; the 4 oldest messages are silently missing and
    the reply has no total or truncation field. Rows are redacted like the other samples.
    """
    raw = json.loads((evidence / "14-all-B-cap.json").read_text(encoding="utf-8"))
    shift = ANCHOR_TIME - NEWEST_OFFSET - newest_created([raw])
    runs = Names("run-{n}")
    runs._seen.update({"run_14cfcbd8edf2": "run-b"})
    envelope = redact_envelope(
        raw, envelope_id="env-cap", runs=runs, messages=Names("{n}"), shift=shift
    )
    rows = envelope["result"]["messages"]
    if len(rows) != 100 or any(r["type"] != "question" for r in rows):
        raise ValueError("the cap sample must hold exactly 100 question rows")
    return {
        "variant": "question-cap-100",
        "description": "exactly 100 question rows, newest first: the shape of a read that hit the 100-row bound",
        "cycles": [envelope],
    }


def write(documents: dict[str, dict], directory: Path = FIXTURES) -> list[Path]:
    paths = []
    for name, document in documents.items():
        path = directory / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args(argv)
    documents = {**build(args.evidence), "question-cap-100": build_cap(args.evidence)}
    for path in write(documents):
        print(f"wrote {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
