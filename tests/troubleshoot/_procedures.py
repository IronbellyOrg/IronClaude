"""R-19 procedure re-implementations (harness §2 + gap-7(b) regex erratum)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

ENUM_TOKEN = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")
_MIDNIGHT = re.compile(r"T00:00:00Z")
FIVE_MIN = timedelta(minutes=5)
_DISC_YES = re.compile(r"discriminator-required\**:\s*yes")
_RERUN = re.compile(r"re-run permitted\**:\s*(yes|no|unknown)")
_TRUNC = re.compile(r"probe-rows-truncated\**:\s*(\d+)")
_INDIST = re.compile(r"indistinguishable\**:")
_DEV_NOISE = re.compile(r"/dev/(null|stdout|stderr|tty|zero)|[0-9]*>\s*/dev/")
_ALLOW_H = re.compile(r"calibrator-eval-cases\.md:(49|54)|escalation-rubric\.md:35")


@dataclass
class Producers:
    observation_kind: str
    rows: list[dict[str, str]]
    count_unknown: bool
    grep_hits: int


@dataclass
class Form:
    hyp_a: str
    hyp_b: str
    observable: str
    probe: str
    reference_value: str
    table: dict[str, tuple[str, str]]
    falsifier: str = ""


def _section(text: str, heading: str) -> str:
    m = re.search(rf"(?m)^## {re.escape(heading)}\s*$", text)
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"(?m)^## ", rest)
    return rest[: nxt.start()] if nxt else rest


def table_rows(md: str, *, include_header: bool = False) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in md.splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        # Consume escaped pipes/backslashes together before splitting delimiters.
        cells = [""]
        for token in re.findall(r"\\[\\|]|[^\\]|\\", s[1:-1]):
            if token == "|":
                cells.append("")
            else:
                cells[-1] += token[1:] if len(token) == 2 else token
        cells = [cell.strip() for cell in cells]
        if cells and re.fullmatch(r":?-{3,}:?", cells[0].replace(" ", "")):
            continue
        if not rows:
            rows.append(cells)
            continue
        if len(rows) == 1 and all(
            re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in cells
        ):
            continue
        rows.append(cells)
    return rows if include_header else rows[1:]


def table_row_by_index(md: str, n: int) -> list[str] | None:
    key = str(n)
    for row in table_rows(md):
        if row and row[0] == key:
            return row
    return None


def _exits_before(src: str, pos: int) -> str:
    head = list(re.finditer(r"(?m)^\s*(?:def |function )", src[:pos]))
    start = head[-1].start() if head else 0
    chunk = src[start:pos]
    found = [
        f"{i}"
        for i, line in enumerate(chunk.splitlines(), 1)
        if re.search(r"\b(return|exit|break)\b", line)
    ]
    return ";".join(found)


def enumerate_producers(sources: dict[str, str], value: str, var: str) -> Producers:
    rows: list[dict[str, str]] = []
    hits = 0
    unknown = False
    pat = re.compile(rf"(?m)^.*(?:{re.escape(value)}|{re.escape(var)}=).*$")
    for name, src in sorted(sources.items()):
        if name.endswith(".md"):
            continue
        unknown = unknown or bool(re.search(rf"{re.escape(var)}=\$\w+-", src))
        mech = re.search(r"(?m)^## Mechanism rows", src)
        body = src if not mech else src[: mech.start()]
        for m in pat.finditer(body):
            hits += 1
            line_no = body[: m.start()].count("\n") + 1
            stmt = m.group(0).strip()
            surviving = "no" if re.match(r"^\s*#", stmt) else "yes"
            rows.append(
                {
                    "id": f"P{hits}",
                    "line": f"{name}:{line_no}",
                    "statement": stmt,
                    "exit_statement": _exits_before(body, m.start()),
                    "marker": "",
                    "walltime": "",
                    "observable": "",
                    "surviving": surviving,
                }
            )
    return Producers("categorical", rows, unknown, hits)


def write_producers_md(p: Producers, out: Path) -> str:
    rows = [dict(row) for row in p.rows]
    audit = []
    if rows and not any(r.get("surviving") == "yes" for r in rows):
        for r in rows:
            audit.append(
                f"- {r['id']} {r['line']}: surviving=re-opened; "
                f"prior surviving={r.get('surviving', '')}; "
                f"prior exit statement={r.get('exit_statement', '')!r} (disputed)"
            )
            r["surviving"] = "yes"
        p.count_unknown = True
    cols = "id | line | statement | exit statement | marker | walltime | observable | surviving"
    lines = [
        f"observation-kind: {p.observation_kind}",
        f"producer-count: {'unknown' if p.count_unknown else len(rows)}",
        "",
        "## Producers",
        f"| {cols} |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            "| "
            + " | ".join(
                r.get(k, "").replace("\\", "\\\\").replace("|", "\\|")
                for k in (
                    "id",
                    "line",
                    "statement",
                    "exit_statement",
                    "marker",
                    "walltime",
                    "observable",
                    "surviving",
                )
            )
            + " |"
        )
    lines.append(f"rows={len(rows)} grep-hits={p.grep_hits}")
    if audit:
        lines.extend(["", "## Contradiction audit", *audit])
    text = "\n".join(lines) + "\n"
    out.write_text(text)
    return text


def producer_rows(producers_md: str) -> int:
    return len(table_rows(_section(producers_md, "Producers")))


def surviving_yes(producers_md: str) -> int:
    n = 0
    for row in table_rows(_section(producers_md, "Producers")):
        cell = row[-1] if row else ""
        if cell in {"surviving=yes", "yes"}:
            n += 1
    return n


def menu_equal(prompt: str, producers_md: str) -> bool:
    def surviving_menu(md: str) -> dict[tuple[str, str], str] | None:
        rows = table_rows(_section(md, "Producers") or md, include_header=True)
        if len(rows) < 2:
            return None
        header, *data = rows
        required = ("id", "line", "statement", "surviving")
        if any(header.count(name) != 1 for name in required):
            return None
        menu = {}
        seen = set()
        for row in data:
            if len(row) != len(header):
                return None
            identity, line, statement, surviving = (
                row[header.index(name)] for name in required
            )
            if (
                not re.fullmatch(r"P[1-9]\d*", identity)
                or not re.fullmatch(r".+:[1-9]\d*", line)
                or not statement
                or surviving not in {"yes", "no", "surviving=yes", "surviving=no"}
                or identity in seen
            ):
                return None
            seen.add(identity)
            if surviving in {"yes", "surviving=yes"}:
                menu[identity, line] = statement
        return menu or None

    expected = surviving_menu(producers_md)
    actual = surviving_menu(prompt)
    if expected is None or actual is None or expected.keys() != actual.keys():
        return False
    # The brief pastes statements verbatim: this preserves every enum value,
    # including repeated/uppercase/computed values, without another enum parser.
    return expected == actual


def primitive_grep(
    files: dict[str, str], producer_files: set[str], patterns: dict[str, str]
) -> list[tuple[str, int, str]]:
    out: list[tuple[str, int, str]] = []
    for name, text in files.items():
        if name not in producer_files:
            continue
        for kind, pat in patterns.items():
            rx = re.compile(pat)
            for i, line in enumerate(text.splitlines(), 1):
                if rx.search(line) and not _DEV_NOISE.search(line):
                    out.append((name, i, kind))
                    if len(out) >= 8:
                        return out
    return out


def overwrite_run_site(locus: str, file_line: str) -> str:
    return re.sub(
        r"(?m)^RUN-SITE:\s*pending-producers",
        f"RUN-SITE: {file_line}",
        locus,
        count=1,
    )


def parse_locus(card: str) -> dict[str, str]:
    keys = ("PRINT-SITE", "RUN-SITE", "SAME-ENV", "OBSERVE-VIA")
    found = {
        k: m.group(1).strip()
        for k in keys
        if (m := re.search(rf"(?m)^{k}:\s*(.*)$", card))
    }
    proofs = re.findall(r"(?m)^CONTROL-PROOF:\s*(.*)$", card)
    if proofs:
        found["CONTROL-PROOF"] = proofs[0].strip()
    return found


def locus_complete(card: str) -> tuple[bool, list[str]]:
    d = parse_locus(card)
    missing = [
        k for k in ("PRINT-SITE", "RUN-SITE", "SAME-ENV", "OBSERVE-VIA") if not d.get(k)
    ]
    if len(re.findall(r"(?m)^(?:## Arm|Arm:)", card)) >= 2:
        if "CONTROL-PROOF" not in d:
            missing.append("CONTROL-PROOF")
    return (not missing, missing)


def derive_same_env(issue_text: str, grounding_text: str = "") -> str:
    blob = issue_text + "\n" + grounding_text
    labels = set(
        re.findall(
            r"(?im)\b(?:runs-on|host|job|runner|env(?:ironment)?|machine|pod|worker)"
            r"[ \t]*[:=][ \t]*(\w[\w./-]*)",
            blob,
        )
    )
    # Keep explicit runner names in prose, not generic 'job failed' statements.
    labels.update(re.findall(r"\brunner[ \t]+(\w+[./-][\w./-]+)", blob, re.I))
    block_indent = None
    for line in blob.splitlines():
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if re.fullmatch(r"[ \t]*(?:runner|env(?:ironment)?|matrix):[ \t]*", line, re.I):
            block_indent = indent
            continue
        bullet = re.fullmatch(r"[ \t]*-[ \t]+(\w[\w./-]*)[ \t]*", line)
        if block_indent is not None and indent > block_indent and bullet:
            labels.add(bullet.group(1))
        else:
            block_indent = None
    if len(labels) > 1:
        return "no"
    if len(labels) == 1:
        return "yes"
    return "unknown"


def requires_runs_in(card: str, same_env: str) -> bool:
    return same_env != "yes" and not re.search(r"(?m)^runs-in[=:]\s*\S+", card)


def verdict_from_log(log: str, marker: str = r"^RESULT:\s*(\w+)") -> str:
    m = re.findall(marker, log, re.M)
    return m[-1] if m else "unobservable"


def parse_discriminator_form(text: str) -> Form:
    def lab(*names: str) -> str:
        for name in names:
            m = re.search(rf"(?im)^{re.escape(name)}:\s*(.*)$", text)
            if m:
                return m.group(1).strip()
        raise ValueError(names[0])

    table: dict[str, tuple[str, str]] = {}
    for row in table_rows(text):
        if len(row) >= 3 and row[0].lower() != "probe result":
            table[row[0]] = (row[1], row[2])
    obs = re.split(r"\s+[—-]", lab("Observable that differs", "Observable"))[0]
    return Form(
        lab("Hypothesis A", "A"),
        lab("Hypothesis B", "B"),
        obs.strip().strip("`"),
        lab("Exact probe", "Probe"),
        lab("Reference-context value", "Reference"),
        table,
        lab("Falsifier") if re.search(r"(?im)^Falsifier:", text) else "",
    )


def outcome_match(form: Form, observed: dict[str, str]) -> tuple[str, str] | None:
    key = observed.get(form.observable)
    if key not in form.table:
        return None
    a, b = form.table[key]
    if a == "consistent" and b == "refuted":
        return ("A", "consistent")
    if b == "consistent" and a == "refuted":
        return ("B", "consistent")
    return ("A", a)


def bracket_trigger(
    error_text: str, producers_md: str, passes_smaller: bool
) -> str | None:
    blob = error_text + producers_md
    if re.search(
        r"\b(limit|max(?:imum)?|too many|exceed\w*)\b[^\n]*\b\d+|\b\d+\b[^\n]*\b(limit|max(?:imum)?)\b",
        blob,
        re.I,
    ):
        return "limit-in-text"
    if passes_smaller:
        return "passes-smaller"
    return None


def bracket(results: dict[int, str], n: int) -> dict:
    seq = [n, n - 2, n - 4, n - 6]
    if not any(results.get(k) == "P" for k in seq):
        seq += [n - 8, n - 10, n - 12]
    if not all(
        results.get(a) != "P" or results.get(b) != "F"
        for a in results
        for b in results
        if a > b
    ):
        return {"status": "UNDETERMINED"}
    passes = [k for k, v in results.items() if v == "P"]
    fails = [k for k, v in results.items() if v == "F"]
    if not passes or not fails:
        return {"status": "UNDETERMINED"}
    p, f = (
        max(passes),
        min(x for x in fails if x > max(passes))
        if any(x > max(passes) for x in fails)
        else min(fails),
    )
    return {"bracket": [p, f], "width": f - p, "guard": p}


def cosmetic_counter(calls: list[str], output_dir: str = "out/") -> list[int]:
    count, fired, exempt = (
        0,
        [],
        re.compile(r"job-[^/]*\.log$|\.stream\.jsonl$|/artifacts/"),
    )
    for i, call in enumerate(calls):
        parts = call.split(None, 1)
        if len(parts) < 2:
            continue
        tool, path = parts[0], parts[1]
        if tool in {"ls", "Write"} or tool.startswith("Bash"):
            continue
        if tool in {"Read", "Glob"} and path.startswith(output_dir):
            if exempt.search(path):
                continue
            count += 1
            if count % 5 == 0:
                fired.append(i + 1)
        elif tool in {"Read", "Bash"} and not path.startswith(output_dir):
            count = 0
    return fired


def counter_key(branch: str, venue_label: str) -> str:
    stripped = re.sub(r"\d+", "", venue_label)
    return f"{branch}:{stripped}"


def bump_rounds(counter_path: Path, key: str, tasklist_md: str) -> int:
    d = json.loads(counter_path.read_text()) if counter_path.exists() else {}
    if _DISC_YES.search(tasklist_md):
        d[key] = d.get(key, 0) + 1
        counter_path.write_text(json.dumps(d))
    return int(d.get(key, 0))


def hardstop_verdict(tasklist_md: str, read_log: list[str]) -> dict:
    n_m = re.search(r"emitters-found:\s*(\d+)", tasklist_md)
    n = int(n_m.group(1)) if n_m else 0
    perm_m = _RERUN.search(tasklist_md)
    perm = perm_m.group(1) if perm_m else ""
    if n >= 1 and perm == "no":
        return {
            "verdict": "blocked-on-authorization",
            "status": "blocked",
            "written": True,
        }
    if n >= 1:
        return {"status": "partial", "task_rows_required": True}
    eligible = [
        f
        for f in read_log
        if re.search(r"\.(log|md|txt|jsonl)$", f)
        and not re.search(r"\.(sh|py|go|ts|js)$", f)
    ]
    if n == 0 and eligible:
        return {"append_to": eligible[-1]}
    return {"capability_verdict": "blocked", "status": "blocked", "source_edit": False}


def timestamp_ok(ts: str, mtime: datetime) -> bool:
    if _MIDNIGHT.search(ts):
        return False
    parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    mt = mtime if mtime.tzinfo else mtime.replace(tzinfo=parsed.tzinfo)
    return parsed <= mt + FIVE_MIN


def differential_decision(table_md: str) -> dict:
    rows = table_rows(table_md)
    if len(rows) < 2 or any("unobserved" in c for r in rows for c in r):
        return {
            "comparator": "none",
            "headline": "UNDETERMINED — no comparator",
            "cap": 0.4,
        }
    fail = next((r for r in rows if "failing" in r[0]), None)
    pas = next((r for r in rows if "passing" in r[0]), None)
    if fail and pas and fail[1] != fail[2] and pas[1] == pas[2]:
        return {"cause_class": "substituted primitive"}
    return {"cause_class": None}


def check_rows(tasklist_md: str, producers_md: str) -> dict:
    body = _section(tasklist_md, "Discriminator rows") or tasklist_md
    pairs: dict[str, set[str]] = {}
    for row in table_rows(body):
        name = re.sub(r"-(exact|ref)$", "", row[0]) if row else ""
        half = (
            "exact"
            if row and row[0].endswith("-exact")
            else "ref"
            if row and row[0].endswith("-ref")
            else ""
        )
        if name and half:
            pairs.setdefault(name, set()).add(half)
    invalid = any(v != {"exact", "ref"} for v in pairs.values())
    if (
        producer_rows(producers_md) >= 1
        and surviving_yes(producers_md) >= 1
        and not pairs
    ):
        invalid = True
    control = any("control" in (r[0] if r else "") for r in table_rows(body))
    trunc_m = _TRUNC.search(tasklist_md)
    truncated = trunc_m.group(1) if trunc_m else ""
    if len(pairs) > 8 and not truncated:
        invalid = True
    distinguishing = any(len(r) > 2 and r[1] != r[2] for r in table_rows(body))
    if not distinguishing and not _INDIST.search(tasklist_md):
        invalid = True
    verdict = None
    if _DISC_YES.search(tasklist_md) and re.search(
        r"verdict:\s*(sufficient|unknown)|discriminator-required",
        tasklist_md,
        re.I,
    ):
        verdict = "partial"
    return {
        "invalid": invalid,
        "control": control,
        "truncated": truncated,
        "distinguishing": distinguishing,
        "verdict": verdict,
        "pairs": len(pairs),
    }


def behaviour_row(card: str, log: list[str]) -> dict:
    rows = table_rows(card)
    if not rows:
        return {"c8_cap": 0.5}
    row = rows[0]
    asserted, query, status = (
        row[2] if len(row) > 2 else "",
        row[4] if len(row) > 4 else "",
        row[5] if len(row) > 5 else "",
    )
    stop = {"the", "code", "or", "clause", "that", "implements", "specifies"}
    query_ok = set(query.split()) <= set(asserted.split()) | stop and not re.search(
        r"format|output|appearance", query, re.I
    )
    order_ok = (
        "write-row" in log
        and "fetch" in log
        and log.index("write-row") < log.index("fetch")
    )
    if status.startswith("recalled"):
        return {"probe_row_appended": True, "query_ok": query_ok, "order_ok": order_ok}
    return {"query_ok": query_ok, "order_ok": order_ok}


def hc_rename_hits(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    rx = re.compile(r"\bH[0-5]\b")
    for p in paths:
        for i, line in enumerate(p.read_text().splitlines(), 1):
            if rx.search(line) and not _ALLOW_H.search(f"{p.name}:{i}"):
                hits.append(f"{p}:{i}")
    return hits


def demo() -> None:
    assert table_rows("| a | b |\n| --- | --- |\n| 1 | 2 |\n") == [["1", "2"]]
    assert counter_key("main", "job12") == "main:job"
    assert verdict_from_log("RESULT: PASS\nRESULT: FAIL\n") == "FAIL"
    print("ok")


if __name__ == "__main__":
    demo()
