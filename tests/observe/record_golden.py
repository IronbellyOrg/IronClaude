"""Developer tool (not shipped): record redacted golden worker-list samples from one live read.

Makes read-only ``worker-list --json --limit 100`` calls through the production runner of
``adapter.py`` (one for the sample, at most two more only to time the call), pipes the decoded
JSON straight into the redaction step and writes four fixture files plus a timing note. The raw
Orca output is never written to disk, logged or printed.

    uv run python tests/observe/record_golden.py --timing-note <path/to/t13-timing.md>

If no Orca CLI validates or the call fails, nothing is written and the exit code is 3.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import time
from pathlib import Path

from superclaude.cli.observe import adapter
from superclaude.cli.observe.parse import format_utc_iso, parse_timestamp

FIXTURES = Path(adapter.__file__).parent / "fixtures"
ANCHOR_TIME = 1794139200.0  # 2026-11-08T12:00:00Z: every timestamp is shifted so the newest lands here
MAX_CALLS = 3  # one sample plus at most two timing repeats (the plan allows five)
SLOW_SECONDS = 3.0

ROW_KEYS = {
    "dispatchId",
    "taskId",
    "runId",
    "workerState",
    "dispatchStatus",
    "terminalState",
    "resource",
    "projection",
}
RESOURCE_KEYS = {
    "id",
    "ownershipState",
    "releaseState",
    "worktreeId",
    "ownerDispatchId",
    "originDispatchId",
    "recoveryAttemptCount",
}
PROJECTION_KEYS = {
    "outcome",
    "role",
    "provider",
    "host",
    "workspace",
    "stage",
    "nextAction",
    "liveness",
    "evidence",
}
LEAK = re.compile(r"/|\\|term_|://|[A-Za-z0-9_+=-]{32,}|[A-Fa-f0-9]{24,}|@")
RULES = [
    "dispatchId, taskId, runId, resource.id, worktreeId, host.id, workspace.id replaced by stable placeholders (w-001, t-001, run-a, res-001, wt-001, host-a, ws-a)",
    "resource.ownerDispatchId and originDispatchId mapped to the dispatch placeholder when they name a collected row, else w-ext-N",
    "stage.detail and stage.activity replaced by fixed synthetic text (free text is never copied)",
    "all timestamps shifted by one constant so the newest lands on 2026-11-08T12:00:00Z; unparsable ones become redacted-time",
    "keys outside the verified worker-list set are kept by name only with the value redacted; page.nextCursor becomes cursor-1; warnings become redacted warning",
    "any remaining string containing a slash, a terminal handle marker, a URL, an at sign or a 24+ character token is replaced by redacted",
]


class Placeholders:
    def __init__(self, prefix: str, width: int = 3, letters: bool = False):
        self.prefix, self.width, self.letters, self.seen = prefix, width, letters, {}

    def __call__(self, value):
        if not isinstance(value, str) or not value:
            return value
        if value not in self.seen:
            n = len(self.seen)
            self.seen[value] = (
                f"{self.prefix}{chr(ord('a') + n % 26) * (n // 26 + 1)}"
                if self.letters
                else f"{self.prefix}{n + 1:0{self.width}d}"
            )
        return self.seen[value]


def shift_times(obj, delta: float):
    """Return ``obj`` with every liveness.observedAt and evidence.lastObservedAt moved by ``delta``."""

    def move(value):
        stamp = parse_timestamp(value)
        return "redacted-time" if stamp is None else format_utc_iso(stamp + delta)

    for row in obj:
        projection = row.get("projection") or {}
        for group, key in (("liveness", "observedAt"), ("evidence", "lastObservedAt")):
            node = projection.get(group)
            if isinstance(node, dict) and key in node and node[key] is not None:
                node[key] = move(node[key])


def scrub(value):
    if isinstance(value, str):
        return "redacted" if LEAK.search(value) else value
    if isinstance(value, dict):
        return {k: scrub(v) for k, v in value.items()}
    if isinstance(value, list):
        return [scrub(v) for v in value]
    return value


def redact(raw: dict) -> dict:
    """Redact one decoded worker-list envelope (a new object; ``raw`` is not kept)."""
    result = raw.get("result") if isinstance(raw, dict) else None
    if not isinstance(result, dict) or not isinstance(result.get("workers"), list):
        raise ValueError("the live reply is not a worker-list envelope")
    dispatch, task, run = (
        Placeholders("w-"),
        Placeholders("t-"),
        Placeholders("run-", letters=True),
    )
    res, wt, host, ws = (
        Placeholders("res-"),
        Placeholders("wt-"),
        Placeholders("host-", letters=True),
        Placeholders("ws-", letters=True),
    )
    workers = [w for w in result["workers"] if isinstance(w, dict)]
    for w in workers:  # first pass: every dispatch id gets its placeholder, in order
        dispatch(w.get("dispatchId"))
    rows = []
    for w in workers:
        row = {}
        for key, value in w.items():
            if key not in ROW_KEYS:
                row[key] = "redacted"  # an unknown key survives by name only
        for key, mapper in (("dispatchId", dispatch), ("taskId", task), ("runId", run)):
            if key in w:
                row[key] = mapper(w[key])
        for key in ("workerState", "dispatchStatus", "terminalState"):
            if key in w:
                row[key] = w[key]
        resource = w.get("resource")
        if isinstance(resource, dict):
            out = {k: "redacted" for k in resource if k not in RESOURCE_KEYS}
            if "id" in resource:
                out["id"] = res(resource["id"])
            if "worktreeId" in resource:
                out["worktreeId"] = wt(resource["worktreeId"])
            for key in ("ownerDispatchId", "originDispatchId"):
                if key in resource:
                    known = (
                        isinstance(resource[key], str)
                        and resource[key] in dispatch.seen
                    )
                    out[key] = dispatch(resource[key]) if known else "w-ext-1"
            for key in ("ownershipState", "releaseState", "recoveryAttemptCount"):
                if key in resource:
                    out[key] = resource[key]
            row["resource"] = out
        projection = w.get("projection")
        if isinstance(projection, dict):
            out = {k: "redacted" for k in projection if k not in PROJECTION_KEYS}
            for key in ("outcome", "role"):
                if key in projection:
                    out[key] = projection[key]
            for group, fields in (
                ("provider", ("id",)),
                ("host", ("kind",)),
                ("workspace", ("kind",)),
                ("stage", ("worker", "dispatch")),
                ("nextAction", ("kind",)),
                ("liveness", ("verdict", "source", "observedAt")),
                ("evidence", ("durable", "liveStatus", "lastObservedAt")),
            ):
                node = projection.get(group)
                if isinstance(node, dict):
                    out[group] = {f: node[f] for f in fields if f in node}
            if isinstance(projection.get("host"), dict) and "id" in projection["host"]:
                out.setdefault("host", {})["id"] = host(projection["host"]["id"])
            if (
                isinstance(projection.get("workspace"), dict)
                and "id" in projection["workspace"]
            ):
                out.setdefault("workspace", {})["id"] = ws(
                    projection["workspace"]["id"]
                )
            stage = projection.get("stage")
            if isinstance(stage, dict):
                for key, text in (
                    ("activity", "redacted activity"),
                    ("detail", "redacted detail"),
                ):
                    if stage.get(key) is not None:
                        out.setdefault("stage", {})[key] = text
            row["projection"] = out
        rows.append(row)
    stamps = [
        parse_timestamp(
            ((r.get("projection") or {}).get("liveness") or {}).get("observedAt")
        )
        for r in rows
    ]
    stamps += [
        parse_timestamp(
            ((r.get("projection") or {}).get("evidence") or {}).get("lastObservedAt")
        )
        for r in rows
    ]
    known = [s for s in stamps if s is not None]
    shift_times(rows, ANCHOR_TIME - max(known) if known else 0.0)
    page = result.get("page") if isinstance(result.get("page"), dict) else {}
    out_page = {k: page[k] for k in ("hasMore", "total", "limit") if k in page}
    if page.get("nextCursor"):
        out_page["nextCursor"] = "cursor-1"
    new = {"workers": rows, "page": out_page}
    scope = result.get("scope")
    if isinstance(scope, dict) and "source" in scope:
        new["scope"] = {"source": scope["source"]}
    counts = result.get("counts")
    if isinstance(counts, dict):
        new["counts"] = {
            k: v for k, v in counts.items() if isinstance(v, (int, float, bool))
        }
    if isinstance(result.get("warnings"), list):
        new["warnings"] = ["redacted warning" for _ in result["warnings"]]
    return {"result": scrub(new)}


def variants(sample: dict) -> dict[str, dict]:
    """The four golden kinds as fixture files: success, missing, stale and contradictory."""

    def wrap(name, description, cycles):
        return {"variant": name, "description": description, "cycles": cycles}

    missing = copy.deepcopy(sample)
    missing["result"].pop("scope", None)
    missing["result"]["page"].pop("total", None)
    first = missing["result"]["workers"][0] if missing["result"]["workers"] else {}
    for group, key in (
        ("liveness", "verdict"),
        ("evidence", "liveStatus"),
        ("nextAction", "kind"),
    ):
        node = (first.get("projection") or {}).get(group)
        if isinstance(node, dict) and key in node:
            del node[key]
            break
    contradictory_1 = copy.deepcopy(sample)
    rows = contradictory_1["result"]["workers"]
    if rows:
        rows.append(copy.deepcopy(rows[0]))  # a duplicate dispatchId
    contradictory_2 = copy.deepcopy(sample)
    first = (
        contradictory_2["result"]["workers"][0]
        if contradictory_2["result"]["workers"]
        else None
    )
    if first is not None:
        live = (first.get("projection") or {}).get("liveness")
        if isinstance(live, dict):
            live["observedAt"] = format_utc_iso(
                ANCHOR_TIME - 86400
            )  # a day older than the first cycle
    fail = {"fail": "timeout"}
    return {
        "golden-success": wrap(
            "golden-success", "one redacted live worker-list read", [sample]
        ),
        "golden-missing": wrap(
            "golden-missing",
            "the sample without result.scope, page.total and one inner projection key",
            [missing],
        ),
        "golden-stale": wrap(
            "golden-stale",
            "the sample, then failing cycles (the test moves the fake monotonic clock past 45 s)",
            [sample, fail, fail, fail],
        ),
        "golden-contradictory": wrap(
            "golden-contradictory",
            "a duplicate dispatchId, then a backward timestamp",
            [contradictory_1, contradictory_2],
        ),
    }


def write_fixture(name: str, data: dict) -> None:
    text = (
        '{\n "variant": '
        + json.dumps(data["variant"])
        + ',\n "description": '
        + json.dumps(data["description"])
        + ',\n "cycles": [\n'
    )
    text += (
        ",\n".join(
            "  " + json.dumps(c, ensure_ascii=True, separators=(",", ":"))
            for c in data["cycles"]
        )
        + "\n ]\n}\n"
    )
    (FIXTURES / f"{name}.json").write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timing-note", required=True)
    args = parser.parse_args()

    orca = adapter._find_orca()
    if orca is None:
        print("BLOCKED: no Orca CLI validated; nothing was recorded", file=sys.stderr)
        return 3
    argv = adapter.build_argv(orca)
    durations: list[float] = []
    sample = None
    for call in range(MAX_CALLS):
        started = time.monotonic()
        try:
            returncode, stdout, _stderr = adapter.production_runner(
                argv, adapter.PER_CALL_TIMEOUT
            )
        except adapter.RunnerFailure as exc:
            print(
                f"BLOCKED: the live call failed ({exc.code}); nothing was recorded",
                file=sys.stderr,
            )
            return 3
        durations.append(time.monotonic() - started)
        if returncode != 0:
            print(
                f"BLOCKED: the live call exited {returncode}; nothing was recorded",
                file=sys.stderr,
            )
            return 3
        if sample is None:
            try:
                sample = redact(
                    json.loads(stdout)
                )  # the raw text is dropped right here
            except ValueError as exc:
                print(f"BLOCKED: {exc}; nothing was recorded", file=sys.stderr)
                return 3
        del stdout
    for name, data in variants(sample).items():
        write_fixture(name, data)

    slowest = max(durations)
    if slowest > SLOW_SECONDS:
        decision = f"raise the per-call timeout to {min(max(3 * slowest, 5.0), 14.0):.1f} s (three times the slowest call, clamped to 5 to 14 s)"
    else:
        decision = f"keep the {adapter.PER_CALL_TIMEOUT:.0f} s default; it stays unmeasured beyond this run (slowest call {slowest:.2f} s)"
    rows = len(sample["result"]["workers"])
    note = [
        "# T13: golden worker-list samples and per-call timing",
        "",
        f"Calls made: {len(durations)} (one for the sample, the rest only to time the call). Rows in the sample: {rows}.",
        "",
        "| Call | Duration (s) |",
        "|---|---|",
        *[f"| {i} | {d:.3f} |" for i, d in enumerate(durations, 1)],
        "",
        f"Slowest: {slowest:.3f} s. Decision: {decision}.",
        "",
        "Redaction rules applied:",
        "",
        *[f"- {rule}" for rule in RULES],
        "",
        "Orca version string: not read (only the two allowed read-only calls are made, and neither reports one).",
        "",
        "Not measured: behaviour under load, a reply with more than one page, a reply with a non-empty `warnings` list unless the sample had one, any failing call. The fixtures were written to `src/superclaude/cli/observe/fixtures/golden-*.json`.",
        "",
    ]
    Path(args.timing_note).write_text("\n".join(note), encoding="utf-8")
    print(
        f"recorded {rows} rows; durations {['%.3f' % d for d in durations]}; decision: {decision}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
