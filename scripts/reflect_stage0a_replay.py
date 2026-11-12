#!/usr/bin/env python3
"""Stage 0a replay: convert the recorded reflect reviewer cards to findings-v2, cluster them and write a report.

Run with ``uv run python scripts/reflect_stage0a_replay.py [--root <repo>] [--out <file>]``. The script reads files
only: it dispatches no model, starts no process and makes no network call.

Inputs (under <root>/.dev/reflect, every directory named pre-*, in name order)
- reviewer-cards/: every regular file directly inside it is a card, except a file whose name contains "calibrat"
  (a calibration sidecar) or whose stem is "summary" (a summary, not a card); both are listed as not read as cards.
  Each card goes through card_convert.convert_card_file, which takes the plan and spec paths from the card or from
  the run's artifacts/input-snapshot.yaml.
- artifacts/input-snapshot.yaml: its file_list (or files) paths, read as card_convert reads them, are the snapshot
  file list given to cluster_v2; a run whose snapshot is missing, unparsable or has no such entries gets an empty
  list, so none of its citations is resolved.
- adversarial/merged-verdict.yaml: its findings are converted with card_convert.convert_card (YAML, the run's
  snapshot paths) and matched against the clusters (see "Agreement" below).
- return-contract.yaml and the files under adversarial/: read for the null convergence scores.

Conversion share (O-7): converted units / units summed over every card (card_convert.summarize); an unlisted
card is one unconverted unit. Since the owner's 2026-11-12 redefinition (conversion-gate-redefinition.md in the
plan package) this share over recorded cards is a descriptive baseline and gates nothing; the report states the
share against the 0.90 reference value as met or not met.

Clusters: per run, one reviewer record per card (reviewer_id = card file stem, ordinal = position in name order); an
unlisted card is passed as an invalid block (it is not a complete reviewer), any other card as the list of its
converted findings. The calibration map holds the numeric confidences found below.

Agreement with the recorded merged verdict (descriptive, seeds no gate): a multi-reviewer cluster is a cluster that
is not chained and holds findings of two or more distinct reviewers. A merged-verdict finding falls in it when
cluster.same_defect_v2 holds between the finding and some member of the cluster. agreement = (merged-verdict findings
that fall in a multi-reviewer cluster) / (merged-verdict findings read), over the runs that have both reviewer cards
and a merged verdict whose findings list could be read; a merged verdict whose findings could not be read is listed.

Null convergence scores: a run's return-contract.yaml counts when tier_reached is 2 and its score key
(adversarial_convergence_score, else convergence_score) is present with a null value. Cause, first rule that holds:
merge_method single-reviewer-fallback -> single-reviewer-fallback; a file under adversarial/ matches SKIP_MARKER ->
skipped-similar debate; merge_method present and not adversarial or single-reviewer-fallback -> illegal merge_method
value; merge_method absent -> other; otherwise (merge_method adversarial, no skip marker) the cause is not determined
and the report says why.

Calibration: a card's sources are its embedded calibration (a top-level calibration mapping in a YAML card, or a
calibration line in a markdown card) and the sidecars in reviewer-cards/ and artifacts/ whose name contains
"calibrat" and does not name t1 or tier1; a sidecar naming reviewer-N applies to the card naming reviewer-N, any
other sidecar to every card of the run. A finding is calibrated when a source gives a number from 0 to 1 for it: in
YAML, per_finding[id].finding_confidence or a bare number at per_finding[id] (per_finding read from the card's section
of the source, directly or under calibration); in markdown, a line naming the id and finding_confidence followed by a
number. Every other finding is uncalibrated. A card's calibration source is embedded, else sidecar, else none.

Every unreadable or unparsable file is counted and listed; none makes the script raise. The report body holds no
timestamp and no absolute path, and every list is sorted, so the same inputs give the same bytes.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from superclaude.cli.review import card_convert as cc
from superclaude.cli.review.cluster import annotate, cluster_v2, same_defect_v2

PLAN_ID = "TASK-WF-implementStages0-20261111-202912"
PLAN_NUMBERS = {"card_dirs": 42, "merged": 33, "nulls": 7}
GATE = 0.90
LEGAL_MERGE = ("adversarial", "single-reviewer-fallback")
CAUSES = (
    "skipped-similar debate",
    "single-reviewer-fallback",
    "illegal merge_method value",
    "other",
    "undetermined",
)
BASELINE_NOTE = (
    "Descriptive baseline: since the owner's 2026-11-12 redefinition this share over recorded cards gates nothing; "
    "the 90% gate applies to cards written under the findings-v2 reviewer brief."
)
SKIP_MARKER = re.compile(
    r"substantially identical|debate (?:was )?skipped|skip(?:s|ped|ping)? (?:the )?debate|debate not reached",
    re.I,
)
TEXT_SUFFIXES = (".md", ".yaml", ".yml", ".txt", ".log", ".json")
_T1 = re.compile(r"(?:^|[-_.])(?:t1|tier1)(?:[-_.]|$)")
_REVIEWER_N = re.compile(r"reviewer-(\d+)")
_MD_EMBEDDED = re.compile(
    r"^\s*(?:<!--\s*|[-*#>]+\s*)?calibration\s*:|\bcalibrated(?:_confidence)?\s*[:=]?\s*\d",
    re.I | re.M,
)


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _yaml(text: str | None) -> tuple[Any, str | None]:
    if text is None:
        return None, "unreadable"
    try:
        return yaml.safe_load(text), None
    except Exception as exc:  # any parser failure is reported, never raised
        return None, f"not parsable ({exc.__class__.__name__})"


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _num(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    value = float(value)
    return value if math.isfinite(value) and 0 <= value <= 1 else None


def _pct(share: float | None) -> str:
    return "n/a" if share is None else f"{share * 100:.2f}%"


def _cell(text: Any) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


# --- calibration -------------------------------------------------------------------------------


def _sidecars(run: Path) -> list[dict]:
    out = []
    for sub in ("reviewer-cards", "artifacts"):
        d = run / sub
        if not d.is_dir():
            continue
        for p in sorted(d.iterdir(), key=lambda p: p.name):
            name = p.name.lower()
            if p.is_file() and "calibrat" in name and not _T1.search(name):
                m = _REVIEWER_N.search(name)
                text = _read(p)
                is_yaml = p.suffix.lower() in (".yaml", ".yml")
                doc, err = _yaml(text) if is_yaml else (None, None)
                out.append(
                    {
                        "path": p,
                        "reviewer": m.group(1) if m else None,
                        "text": text if not is_yaml else None,
                        "doc": doc,
                        "error": err
                        if is_yaml
                        else (None if text is not None else "unreadable"),
                    }
                )
    return out


def _section(doc: Any, card: Path) -> Any:
    """The part of a run-level calibration document that belongs to the card, in document order, or None."""
    m = _REVIEWER_N.search(card.name)
    keys = {card.stem, card.name}
    if m:
        keys |= {f"reviewer-{m.group(1)}", f"reviewer_{m.group(1)}"}
    if isinstance(doc, dict):
        for k in ("card", "file", "path"):
            v = doc.get(k)
            if isinstance(v, str) and PurePosixPath(v).name == card.name:
                return doc
        for k, v in doc.items():
            if str(k) in keys and isinstance(v, dict):
                return v
        children = list(doc.values())
    elif isinstance(doc, list):
        children = doc
    else:
        return None
    for v in children:
        found = _section(v, card)
        if found is not None:
            return found
    return None


def _per_finding_entry(section: Any, fid: str) -> tuple[bool, float | None]:
    """(an entry exists, its numeric confidence or None) for fid in the section's per_finding."""
    if not isinstance(section, dict):
        return False, None
    for scope in (section, section.get("calibration")):
        if not isinstance(scope, dict) or "per_finding" not in scope:
            continue
        pf = scope["per_finding"]
        entry: Any = None
        found = False
        if isinstance(pf, dict) and fid in {str(k) for k in pf}:
            entry = next(v for k, v in pf.items() if str(k) == fid)
            found = True
        elif isinstance(pf, list):
            for item in pf:
                if isinstance(item, dict) and str(item.get("id")) == fid:
                    entry, found = item, True
                    break
        if found:
            value = (
                entry.get("finding_confidence") if isinstance(entry, dict) else entry
            )
            return True, _num(value)
    return False, None


def _md_confidence(text: str | None, fid: str) -> float | None:
    if not text:
        return None
    pat = re.compile(
        rf"(?<![\w-]){re.escape(fid)}(?![\w-])[^\n]*?finding_confidence\W{{0,5}}([01](?:\.\d+)?)"
    )
    m = pat.search(text)
    return _num(float(m.group(1))) if m else None


def _card_calibration(card: Path, sidecars: list[dict], findings: list[dict]) -> dict:
    """Calibration source of a card and, per finding id, (status, confidence)."""
    sources: list[tuple[str, str, Any]] = []  # (label, kind, payload)
    text = _read(card)
    if card.suffix.lower() in (".yaml", ".yml"):
        doc, _ = _yaml(text)
        if isinstance(doc, dict) and doc.get("calibration") is not None:
            sources.append(("embedded", "section", doc.get("calibration")))
    elif text and _MD_EMBEDDED.search(text):
        sources.append(("embedded", "text", text))
    m = _REVIEWER_N.search(card.name)
    number = m.group(1) if m else None
    for sc in sidecars:
        if sc["reviewer"] is not None and sc["reviewer"] != number:
            continue
        if sc["text"] is not None:
            sources.append(("sidecar", "text", sc["text"]))
        elif sc["reviewer"] is not None:
            sources.append(("sidecar", "section", sc["doc"]))
        else:
            sources.append(("sidecar", "section", _section(sc["doc"], card)))
    per: dict[str, tuple[str, float | None]] = {}
    for f in findings:
        fid = f.get("id")
        status, conf = "no entry", None
        for _, kind, payload in sources:
            if kind == "text":
                conf = _md_confidence(payload, fid)
                found = conf is not None
            else:
                found, conf = _per_finding_entry(payload, fid)
            if conf is not None:
                status = "numeric"
                break
            if found:
                status = "non-numeric entry"
        per[fid] = (status, conf)
    return {"source": sources[0][0] if sources else "none", "per_finding": per}


# --- runs --------------------------------------------------------------------------------------


def _card_files(cards_dir: Path) -> tuple[list[Path], list[tuple[str, str]]]:
    cards, skipped = [], []
    for p in sorted(cards_dir.iterdir(), key=lambda p: p.name):
        if not p.is_file():
            skipped.append((p.name, "not a regular file"))
        elif "calibrat" in p.name.lower():
            skipped.append((p.name, "calibration sidecar"))
        elif p.stem.lower() == "summary":
            skipped.append((p.name, "summary, not a card"))
        else:
            cards.append(p)
    return cards, skipped


def _snapshot(run: Path) -> tuple[list[str], str]:
    path = run / cc.SNAPSHOT
    if not path.is_file():
        return [], "missing"
    doc, err = _yaml(_read(path))
    if err:
        return [], err
    paths = sorted(
        {
            e["path"]
            for e in cc._snapshot_entries(doc)
            if isinstance(e, dict) and isinstance(e.get("path"), str)
        }
    )
    return paths, "present" if paths else "no file_list or files entries"


def _merged(
    run: Path, snapshot_paths: list[str], card_records: list[tuple], cluster_out: dict
) -> dict | None:
    path = run / "adversarial" / "merged-verdict.yaml"
    if not path.is_file():
        return None
    text = _read(path)
    if text is None:
        return {"read": False, "reason": "unreadable", "total": 0, "inside": 0}
    plan, spec = cc.snapshot_paths(run / cc.SNAPSHOT)
    res = cc.convert_card(text, fmt="yaml", plan_path=plan, spec_path=spec)
    if res["shape"] == "unlisted":
        return {
            "read": False,
            "reason": res["problems"][0]["reason"],
            "total": 0,
            "inside": 0,
        }
    snap = set(snapshot_paths)
    views = {
        (rid, f["id"]): annotate(f, snap)
        for rid, _, block, _ in card_records
        if isinstance(block, list)
        for f in block
    }
    multi = [
        [views[(m["reviewer_id"], m["id"])] for m in c["members"]]
        for c in cluster_out["clusters"]
        if not c["chained"] and len(c["reviewers"]) >= 2
    ]
    inside = 0
    for f in res["findings"]:
        view = annotate(f, snap)
        if any(same_defect_v2(view, m) for members in multi for m in members):
            inside += 1
    return {
        "read": True,
        "reason": None,
        "total": res["counts"]["units"],
        "inside": inside,
        "multi_clusters": len(multi),
    }


def _null_contract(run: Path, root: Path) -> dict | None:
    """A null-score record for the run's return contract, a parse-problem record, or None when it does not count."""
    path = run / "return-contract.yaml"
    if not path.is_file():
        return None
    text = _read(path)
    doc, err = _yaml(text)
    if err or not isinstance(doc, dict):
        return {"run": run.name, "problem": err or "not a mapping"}
    key = (
        "adversarial_convergence_score"
        if "adversarial_convergence_score" in doc
        else "convergence_score"
        if "convergence_score" in doc
        else None
    )
    tier = doc.get("tier_reached")
    record = {"run": run.name, "tier": tier, "score_key": key}
    if not (tier == 2 and not isinstance(tier, bool)):
        record["counts"] = False
        record["null"] = key is not None and doc.get(key) is None
        return record
    if key is None:
        record["counts"] = False
        record["no_score_key"] = True
        return record
    if doc.get(key) is not None:
        record["counts"] = False
        return record
    record["counts"] = True
    has_mm = "merge_method" in doc
    mm = doc.get("merge_method")
    notes = []
    for k in ("merge_method", key):
        m = re.search(rf'^\s*"?{k}"?\s*:[^#\n]*#\s*(.+)$', text or "", re.M)
        if m:
            notes.append(f"{k}: {m.group(1).strip()}")
    adv = run / "adversarial"
    hits: list[str] = []
    searched = unreadable = 0
    if adv.is_dir():
        for p in sorted(adv.rglob("*"), key=lambda p: p.as_posix()):
            if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES:
                searched += 1
                body = _read(p)
                if body is None:
                    unreadable += 1
                    continue
                for n, line in enumerate(body.splitlines(), 1):
                    if SKIP_MARKER.search(line):
                        hits.append(f"{_rel(p, root)}:{n}")
    if mm == "single-reviewer-fallback":
        cause, why = (
            "single-reviewer-fallback",
            "merge_method is single-reviewer-fallback",
        )
    elif hits:
        cause, why = "skipped-similar debate", "skip marker at " + ", ".join(hits[:3])
    elif has_mm and mm not in LEGAL_MERGE:
        cause, why = "illegal merge_method value", f"merge_method is {mm!r}"
    elif not has_mm:
        cause, why = (
            "other",
            "merge_method is absent from the contract (no merge recorded)",
        )
    elif not adv.is_dir():
        cause = "undetermined"
        why = (
            "merge_method is adversarial and the run has no adversarial/ directory, so a skipped debate cannot be "
            "told apart from a failed or unrecorded one"
        )
    else:
        cause = "undetermined"
        why = (
            f"merge_method is adversarial and none of the {searched} text file(s) under adversarial/ holds a skip "
            "marker, so a skipped debate cannot be told apart from a failed or unrecorded one"
        )
    if unreadable:
        why += f" ({unreadable} file(s) under adversarial/ could not be read)"
    record.update(
        merge_method=mm if has_mm else "(absent)",
        cause=cause,
        why=why,
        notes=notes,
        adversarial_dir=adv.is_dir(),
        files_searched=searched,
    )
    return record


def collect(root: Path) -> dict:
    """Everything the report shows, from the files under root/.dev/reflect."""
    base = root / ".dev" / "reflect"
    runs = (
        sorted((p for p in base.glob("pre-*") if p.is_dir()), key=lambda p: p.name)
        if base.is_dir()
        else []
    )
    data: dict[str, Any] = {
        "runs": len(runs),
        "card_runs": [],
        "cards": [],
        "skipped_files": [],
        "contracts": [],
    }
    for run in runs:
        contract = _null_contract(run, root)
        if contract is not None:
            data["contracts"].append(contract)
        cards_dir = run / "reviewer-cards"
        if not cards_dir.is_dir():
            continue
        cards, skipped = _card_files(cards_dir)
        data["skipped_files"] += [
            (_rel(cards_dir / n, root), why) for n, why in skipped
        ]
        snapshot, snap_state = _snapshot(run)
        sidecars = _sidecars(run)
        records = []
        for ordinal, card in enumerate(cards):
            res = cc.convert_card_file(card)
            cal = _card_calibration(card, sidecars, res["findings"])
            listed = res["shape"] != "unlisted"
            calmap = {
                fid: conf
                for fid, (_, conf) in cal["per_finding"].items()
                if conf is not None
            }
            records.append(
                (card.stem, ordinal, res["findings"] if listed else None, calmap)
            )
            data["cards"].append(
                {
                    "run": run.name,
                    "card": _rel(card, root),
                    "result": res,
                    "calibration": cal,
                }
            )
        out = cluster_v2(records, snapshot)
        merged = _merged(run, snapshot, records, out)
        data["card_runs"].append(
            {
                "run": run.name,
                "cards": len(cards),
                "snapshot": snap_state,
                "cluster": out,
                "merged": merged,
                "sidecar_errors": [
                    (_rel(sc["path"], root), sc["error"])
                    for sc in sidecars
                    if sc["error"]
                ],
            }
        )
    data["summary"] = cc.summarize(c["result"] for c in data["cards"])
    return data


# --- report ------------------------------------------------------------------------------------


def _cause_key(reason: str) -> str:
    reason = re.sub(r"'[^']*'", "'...'", reason)
    return re.sub(r"\d+", "N", reason)


def render(data: dict) -> str:
    s = data["summary"]
    share = s["share"]
    passed = share is not None and share >= GATE
    card_runs = data["card_runs"]
    merged_runs = [r for r in card_runs if r["merged"] is not None]
    no_snapshot = [r for r in card_runs if r["snapshot"] != "present"]
    own = [r for r in card_runs if PLAN_ID in r["run"]]
    findings_total = s["units"] - s["by_shape"]["unlisted"]["units"]
    lines: list[str] = []
    a = lines.append
    a("# Stage 0a replay report: recorded reflect reviewer cards")
    a("")
    a(
        "Generated by `uv run python scripts/reflect_stage0a_replay.py`. Zero dispatch: the script reads files only "
        "(no model, no process, no network). Descriptive and unseeded; the conversion share over recorded cards is a baseline, not a gate."
    )
    a("")
    a("## Inputs")
    a("")
    a(f"- `pre-*` run directories under `.dev/reflect`: {data['runs']}")
    a(
        f"- with a `reviewer-cards/` directory: {len(card_runs)} (the plan and spec say {PLAN_NUMBERS['card_dirs']}; "
        f"difference {len(card_runs) - PLAN_NUMBERS['card_dirs']:+d})"
    )
    a(
        f"- of those, with `adversarial/merged-verdict.yaml`: {len(merged_runs)} (the plan and spec say "
        f"{PLAN_NUMBERS['merged']}; difference {len(merged_runs) - PLAN_NUMBERS['merged']:+d})"
    )
    a(
        f"- of those, runs whose name contains this plan's id `{PLAN_ID}` (its own reflect run, recorded after the "
        f"spec's count): {len(own)}"
        + (f" ({', '.join('`' + r['run'] + '`' for r in own)})" if own else "")
    )
    a(
        f"- card-directory runs without a usable `artifacts/input-snapshot.yaml` (missing, unparsable, or no "
        f"`file_list`/`files` entries, the keys card_convert reads): {len(no_snapshot)} of {len(card_runs)}; "
        "cluster_v2 gets an empty snapshot list for them, so none of their citations is resolved"
    )
    a(
        f"- card files read: {s['cards']}; files in `reviewer-cards/` not read as cards: {len(data['skipped_files'])}"
    )
    a("")
    if no_snapshot:
        a(
            "Runs without a usable snapshot: "
            + ", ".join(f"`{r['run']}` ({r['snapshot']})" for r in no_snapshot)
            + "."
        )
        a("")
    if data["skipped_files"]:
        a("Files in `reviewer-cards/` not read as cards:")
        a("")
        for path, why in sorted(data["skipped_files"]):
            a(f"- `{path}`: {why}")
        a("")
    a("## Conversion share (O-7, baseline)")
    a("")
    a(
        "Unit = one finding of a listed card, or one whole unlisted card (Task 2 rule: an unconvertible card lowers "
        "the share instead of leaving the denominator). A unit converts unambiguously when every citation has a "
        "`(path, line)` and the line passes the findings-v2 checker."
    )
    a("")
    a(
        f"- Units: {s['units']} ({findings_total} findings in listed cards + {s['by_shape']['unlisted']['units']} unlisted cards)"
    )
    a(f"- Converted unambiguously: {s['converted']}; unconverted: {s['unconverted']}")
    a(f"- Conversion share: {s['converted']}/{s['units']} = {_pct(share)}")
    a(f"- Reference value (at least 90%): {'met' if passed else 'not met'}; no gate")
    a(
        f"- Refs: {s['refs']} citations, {s['refs_resolved']} with a path and line, {s['refs_unresolved']} unresolved"
    )
    a("")
    a(f"**{BASELINE_NOTE}**")
    a("")
    a("### Cards by shape (Task 2 card-format table)")
    a("")
    a("| Shape | Cards | Units | Converted | Unconverted | Share |")
    a("|---|---:|---:|---:|---:|---:|")
    for shape in cc.SHAPES:
        b = s["by_shape"][shape]
        a(
            f"| {shape} | {b['cards']} | {b['units']} | {b['converted']} | {b['units'] - b['converted']} | {_pct(b['share'])} |"
        )
    a("")
    a("### Unconverted units by cause")
    a("")
    causes: Counter = Counter()
    cit_causes: Counter = Counter()
    for c in data["cards"]:
        r = c["result"]
        unit_cause = "unlisted card: " if r["shape"] == "unlisted" else ""
        by_id = {f["id"]: f for f in r["findings"]}
        for p in r["problems"]:
            reasons = sorted(
                {
                    cit.get("reason", "")
                    for cit in by_id.get(p["id"], {}).get("citations", [])
                    if cit.get("role") == "unresolved"
                }
            )
            if reasons:
                causes["unresolved citation: " + "; ".join(reasons)] += 1
            else:
                causes[unit_cause + _cause_key(p["reason"])] += 1
        for f in r["findings"]:
            for cit in f["citations"]:
                if cit.get("role") == "unresolved":
                    cit_causes[cit.get("reason", "")] += 1
    a("| Cause | Units |")
    a("|---|---:|")
    for cause, n in sorted(causes.items(), key=lambda kv: (-kv[1], kv[0])):
        a(f"| {_cell(cause)} | {n} |")
    a("")
    a("Unresolved citations by reason (a finding can hold several):")
    a("")
    a("| Reason | Citations |")
    a("|---|---:|")
    for cause, n in sorted(cit_causes.items(), key=lambda kv: (-kv[1], kv[0])):
        a(f"| {_cell(cause)} | {n} |")
    a("")
    a("### Unconvertible cards (shape unlisted)")
    a("")
    unl = [c for c in data["cards"] if c["result"]["shape"] == "unlisted"]
    if not unl:
        a("None.")
    for c in sorted(unl, key=lambda c: c["card"]):
        a(f"- `{c['card']}`: {c['result']['problems'][0]['reason']}")
    a("")
    a("### Per card")
    a("")
    a("| Card | Shape | Units | Converted | Share | Calibration source |")
    a("|---|---|---:|---:|---:|---|")
    for c in sorted(data["cards"], key=lambda c: c["card"]):
        k = c["result"]["counts"]
        a(
            f"| `{c['card']}` | {c['result']['shape']} | {k['units']} | {k['converted']} | {_pct(k['share'])} | "
            f"{c['calibration']['source']} |"
        )
    a("")
    a("## Clusters (cluster_v2)")
    a("")
    tot = Counter()
    for r in card_runs:
        o = r["cluster"]
        tot["runs"] += 1
        tot["clusters"] += len(o["clusters"])
        tot["multi"] += sum(1 for c in o["clusters"] if len(c["reviewers"]) >= 2)
        tot["multi_unchained"] += sum(
            1 for c in o["clusters"] if len(c["reviewers"]) >= 2 and not c["chained"]
        )
        tot["chained"] += len(o["chained"])
        tot["blocking"] += o["blocking_clusters"]
        tot["singletons"] += sum(1 for c in o["clusters"] if len(c["members"]) == 1)
        tot["members"] += sum(len(c["members"]) for c in o["clusters"])
        for k, v in o["citations"].items():
            tot["cit_" + k] += v
        tot["problems"] += len(o["problems"])
    a(
        f"Totals over {tot['runs']} runs: {tot['members']} clustered findings, {tot['clusters']} clusters, "
        f"{tot['singletons']} single-finding clusters, {tot['multi']} clusters holding two or more reviewers "
        f"({tot['multi_unchained']} not chained), {tot['chained']} chained, {tot['blocking']} blocking. Citations: "
        f"{tot['cit_resolved']} resolved against the snapshot, {tot['cit_unresolved']} unresolved (path not in the "
        f"snapshot list), {tot['cit_malformed']} malformed (the converter's unresolved refs). Input problems "
        f"reported by cluster_v2: {tot['problems']}."
    )
    a("")
    a(
        "cluster_agreement (telemetry only) is null when fewer than 2 reviewers are complete, or when there are "
        "blocking clusters but none of them is unchained with a calibrated support value."
    )
    a("")
    a(
        "| Run | Cards | Complete | Snapshot | Findings | Clusters | Multi-reviewer | Chained | Blocking | Resolved / unresolved / malformed citations | cluster_agreement |"
    )
    a("|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|")
    for r in card_runs:
        o = r["cluster"]
        ca = o["cluster_agreement"]
        a(
            f"| `{r['run']}` | {r['cards']} | {o['valid_blocks']} | {r['snapshot']} | "
            f"{sum(len(c['members']) for c in o['clusters'])} | {len(o['clusters'])} | "
            f"{sum(1 for c in o['clusters'] if len(c['reviewers']) >= 2)} | {len(o['chained'])} | {o['blocking_clusters']} | "
            f"{o['citations']['resolved']} / {o['citations']['unresolved']} / {o['citations']['malformed']} | "
            f"{'null' if ca is None else f'{ca:.4f}'} |"
        )
    a("")
    a("## Agreement with the recorded merged verdict (descriptive)")
    a("")
    a(
        "Formula: agreement = (recorded merged-verdict findings that fall in a multi-reviewer cluster) / "
        "(recorded merged-verdict findings read). A multi-reviewer cluster is a cluster that is not chained and holds "
        "findings of two or more distinct reviewers; a merged-verdict finding falls in it when `same_defect_v2` holds "
        "between that finding (converted with card_convert and the run's snapshot paths) and some member of the "
        "cluster. Merged verdicts whose findings list could not be read are listed and add nothing to either side. "
        "This number is descriptive and seeds no gate."
    )
    a("")
    read = [r for r in merged_runs if r["merged"]["read"]]
    inside = sum(r["merged"]["inside"] for r in read)
    total = sum(r["merged"]["total"] for r in read)
    a(
        f"- Merged verdicts read: {len(read)} of {len(merged_runs)}; findings read: {total}; "
        f"falling in a multi-reviewer cluster: {inside}; agreement: {inside}/{total} = "
        f"{_pct(inside / total if total else None)}"
    )
    a("")
    a(
        "| Run | Merged findings | In a multi-reviewer cluster | Multi-reviewer clusters | Agreement |"
    )
    a("|---|---:|---:|---:|---:|")
    for r in read:
        m = r["merged"]
        a(
            f"| `{r['run']}` | {m['total']} | {m['inside']} | {m['multi_clusters']} | "
            f"{_pct(m['inside'] / m['total'] if m['total'] else None)} |"
        )
    a("")
    unread = [r for r in merged_runs if not r["merged"]["read"]]
    if unread:
        a("Merged verdicts whose findings could not be read:")
        a("")
        for r in unread:
            a(f"- `{r['run']}`: {r['merged']['reason']}")
        a("")
    a("## Recorded null convergence scores")
    a("")
    counted = [c for c in data["contracts"] if c.get("counts")]
    problems = [c for c in data["contracts"] if "problem" in c]
    no_key = [c for c in data["contracts"] if c.get("no_score_key")]
    t1_null = [
        c
        for c in data["contracts"]
        if not c.get("counts") and c.get("null") and "problem" not in c
    ]
    a(
        "Counted: a run's `return-contract.yaml` with `tier_reached: 2` whose score key "
        "(`adversarial_convergence_score`, else `convergence_score`) is present with a null value. Cause, first rule "
        "that holds: `merge_method: single-reviewer-fallback`; a skip marker (`variants substantially identical`, "
        "`debate skipped`, `skip debate`, `debate not reached`) in a file under the run's `adversarial/`; a "
        "`merge_method` that is present but not `adversarial` or `single-reviewer-fallback` (illegal value); "
        "`merge_method` absent (other); otherwise undetermined."
    )
    a("")
    a(
        f"Found {len(counted)} null scores (the plan and spec say {PLAN_NUMBERS['nulls']}; difference "
        f"{len(counted) - PLAN_NUMBERS['nulls']:+d}). Return contracts read: {len(data['contracts'])}."
    )
    a("")
    a("| Run | merge_method | Score key | Cause | Evidence | Contract notes |")
    a("|---|---|---|---|---|---|")
    for c in counted:
        a(
            f"| `{c['run']}` | `{_cell(c['merge_method'])}` | `{c['score_key']}` | {c['cause']} | {_cell(c['why'])} | "
            f"{_cell('; '.join(c['notes'])) or '-'} |"
        )
    a("")
    by_cause = Counter(c["cause"] for c in counted)
    a("By cause: " + ", ".join(f"{k} {by_cause.get(k, 0)}" for k in CAUSES) + ".")
    a("")
    und = [c for c in counted if c["cause"] == "undetermined"]
    if und:
        a("Cause not determined:")
        a("")
        for c in und:
            a(f"- `{c['run']}`: {c['why']}.")
    else:
        a("Every counted null score has a determined cause.")
    a("")
    if no_key:
        a(
            "Tier-2 contracts with no score key at all (not counted as null): "
            + ", ".join(f"`{c['run']}`" for c in no_key)
            + "."
        )
        a("")
    if t1_null:
        a(
            "Null scores outside tier 2 (not counted): "
            + ", ".join(f"`{c['run']}`" for c in t1_null)
            + "."
        )
        a("")
    if problems:
        a(
            "Return contracts that could not be read: "
            + ", ".join(f"`{c['run']}` ({c['problem']})" for c in problems)
            + "."
        )
        a("")
    a("## Recorded calibration")
    a("")
    a(
        "A finding is calibrated only when a source gives a numeric confidence from 0 to 1 for its id "
        "(`per_finding[id].finding_confidence`, or a bare number at `per_finding[id]`, in the card's section of an "
        "embedded block or sidecar; in markdown, a line naming the id with `finding_confidence` and a number). "
        "Source of a card: embedded, else sidecar, else none. Findings of unlisted cards are not counted (they have "
        "no findings)."
    )
    a("")
    by_source: dict[str, Counter] = {
        k: Counter() for k in ("embedded", "sidecar", "none")
    }
    for c in data["cards"]:
        src = c["calibration"]["source"]
        by_source[src]["cards"] += 1
        for status, _ in c["calibration"]["per_finding"].values():
            by_source[src]["findings"] += 1
            by_source[src][status] += 1
    a(
        "| Source | Cards | Findings | Calibrated (numeric) | Uncalibrated: non-numeric entry | Uncalibrated: no entry |"
    )
    a("|---|---:|---:|---:|---:|---:|")
    for src, k in by_source.items():
        a(
            f"| {src} | {k['cards']} | {k['findings']} | {k['numeric']} | {k['non-numeric entry']} | {k['no entry']} |"
        )
    uncal = sum(k["non-numeric entry"] + k["no entry"] for k in by_source.values())
    a("")
    a(
        f"Uncalibrated findings: {uncal} of {sum(k['findings'] for k in by_source.values())}."
    )
    a("")
    sidecar_errors = sorted({e for r in card_runs for e in r["sidecar_errors"]})
    if sidecar_errors:
        a(
            "Calibration sidecars that could not be read: "
            + ", ".join(f"`{p}` ({e})" for p, e in sidecar_errors)
            + "."
        )
        a("")
    a("Uncalibrated findings by card (source: ids):")
    a("")
    for c in sorted(data["cards"], key=lambda c: c["card"]):
        ids = [
            fid
            for fid, (status, _) in c["calibration"]["per_finding"].items()
            if status != "numeric"
        ]
        if ids:
            a(f"- `{c['card']}` ({c['calibration']['source']}): {', '.join(ids)}")
    a("")
    return "\n".join(lines)


def default_out(root: Path) -> Path:
    package = root / ".dev" / "tasks" / "to-do" / PLAN_ID
    return (
        package / "artifacts" / "stage0a-report.md"
        if package.is_dir()
        else Path("artifacts") / "stage0a-report.md"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="report file (default: the plan package artifact)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    out = args.out or default_out(root)
    data = collect(root)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data), encoding="utf-8")
    s = data["summary"]
    print(f"wrote {out}")
    print(
        f"cards={s['cards']} units={s['units']} converted={s['converted']} share={_pct(s['share'])} (baseline, no gate)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
