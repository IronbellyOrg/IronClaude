#!/usr/bin/env python3
"""Stage 2 shadow-exit aggregator for the reflect Tier 2 panel (Stage 2 exit: 20 shadow runs).

Run with ``uv run python scripts/reflect_shadow_exit.py [--runs-root <dir>] [--required 20] [--out <file>]``. It reads
files only (no model, no process, no network) and writes only the optional ``--out`` report.

Shadow runs: every ``<runs-root>/pre-*/panel/manifest.json`` whose ``t2_engine_effective`` is ``shadow``. A manifest in
state ``published`` is counted; ``failed`` fails the exit; any other state is an incomplete run, listed and not
counted. The legacy baseline is the recorded 1.8.0 pre runs without ``panel/manifest.json`` (the set of
``scripts/reflect_verdict_replay.py``).

Per counted run the script joins ``return-contract.yaml`` and ``adversarial/merged-verdict.yaml`` and checks:
- panel parity, recomputed (the recorded boolean is not trusted): the ordered ``(persona, model class)`` lists of
  ``panel/resolution.json`` (persona by resolution order: analyzer, qa, refactorer; model ids mapped through the tier
  file's ``classes``), of the reviewer card headers (``persona:``, ``model_class:``, ``model:`` in
  ``panel/cards/reviewer-<N>.md``, whose ``model`` must equal the resolved id) and of the legacy rotation as run
  (the contract's ``reviewer_personas`` and ``reviewer_models``, each model mapped to a class) must be equal. A run
  whose recorded ``panel_parity`` is true and whose recomputed value is false is also reported as a wrong record;
- MALFORMED: the number of ``audit.log`` rows that contain the word MALFORMED (the EV-1 / EV-2 row of SKILL.md);
- the panel contract lint (``panel_lint.lint_panel_contract``); any line fails the run. The matched legacy contract
  passed to it is the run's own contract, because in shadow mode the legacy builder writes the contract: its parity
  fields (L7) are then trivially equal, and the parity that matters is the recomputed ``panel_parity``;
- the verdict replay (``derive_verdict`` with ``expected_tier=2``, ``child_rc=0``, both ``allow_single_vendor``
  values) against the legacy baseline; any new degraded reason fails.

Aggregates: the run count against ``--required``; MALFORMED total (must be zero); the EV-1 failure rate of the shadow
runs against the legacy baseline, both under the same rule (``len(reviewer_cards)``; manifest counts are not used),
over the runs where Wave 4 ran (``tier_reached`` is not 1), each with its n (the shadow rate must be no higher); the
Stage 2 counts: 2-of-3 shortfalls (manifest ``reviewers_resolved`` 3 and ``reviewers_complete`` 2), runs with an
unknown executor class (``executor_class_resolved`` false), the mean findings-block compliance rate and the
``cluster_agreement`` distribution (``n/a`` when empty).

Overall line: FAIL when any run or aggregate check fails; else INSUFFICIENT-RUNS when fewer than ``--required`` runs
were counted; else PASS. Exit codes: 0 PASS, 1 FAIL, 3 INSUFFICIENT-RUNS, 2 usage error.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

import yaml

from superclaude.cli.reflect import panel_lint as pl
from superclaude.cli.review import manifest as mf
from superclaude.cli.review import panel as pnl

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RUNS = 20
PERSONAS = ("analyzer", "qa", "refactorer")
EXIT = {"PASS": 0, "FAIL": 1, "INSUFFICIENT-RUNS": 3}
_MALFORMED = re.compile(r"\bMALFORMED\b")
_CARD = re.compile(r"^reviewer-(\d+)\.md$")


def _load_replay():
    spec = importlib.util.spec_from_file_location(
        "reflect_verdict_replay", Path(__file__).with_name("reflect_verdict_replay.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rv = _load_replay()


def _yaml_map(path: Path) -> dict | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError):
        return None
    return data if isinstance(data, dict) else None


def _json_map(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def tele(contract: dict, key: str) -> Any:
    """A non-stable field, from the nested telemetry block or (older runs) the top level."""
    block = contract.get("telemetry")
    if isinstance(block, dict) and key in block:
        return block[key]
    return contract.get(key)


def card_headers(run: Path) -> list[dict[str, str]]:
    """The header fields of panel/cards/reviewer-<N>.md in numeric order (the lines before the first blank line)."""
    cards = run / "panel" / "cards"
    found = []
    if cards.is_dir():
        for p in cards.iterdir():
            m = _CARD.match(p.name)
            if m and p.is_file():
                found.append((int(m.group(1)), p))
    out = []
    for _, p in sorted(found):
        try:
            head = p.read_text(encoding="utf-8").split("\n\n", 1)[0]
        except (OSError, ValueError):
            head = ""
        out.append(dict(row.split(": ", 1) for row in head.splitlines() if ": " in row))
    return out


def recompute_parity(
    run: Path, contract: dict, classes: dict, tiers_sha256: str | None = None
) -> tuple[bool, str]:
    """(parity, reason): the three ordered (persona, model class) lists must exist and be equal.

    With tiers_sha256 (the hash of the tier file `classes` came from), a run whose resolution recorded a different
    hash is not interpreted with today's mapping: it is reported as not proven, with that reason.
    """
    resolution = _json_map(run / "panel" / "resolution.json")
    if resolution is None or not isinstance(resolution.get("reviewers"), list):
        return False, "panel/resolution.json is missing or has no reviewers"
    if tiers_sha256 is not None and resolution.get("tiers_sha256") != tiers_sha256:
        return (
            False,
            "the run's tier file hash differs from the current tier file, so its model ids cannot be mapped to classes here",
        )
    reviewers = resolution["reviewers"]
    resolved = [
        (PERSONAS[i] if i < len(PERSONAS) else None, classes.get(r.get("model")))
        for i, r in enumerate(reviewers)
    ]
    heads = card_headers(run)
    if len(heads) != len(reviewers):
        return (
            False,
            f"{len(heads)} card header(s) for {len(reviewers)} resolved reviewer(s)",
        )
    cards = []
    for h, r in zip(heads, reviewers):
        if not {"persona", "model_class", "model"} <= set(h):
            return False, "a card header lacks persona:, model_class: or model:"
        if h["model"] != r.get("model"):
            return (
                False,
                f"card model {h['model']!r} differs from the resolved {r.get('model')!r}",
            )
        cards.append((h["persona"], h["model_class"]))
    personas, models = (
        tele(contract, "reviewer_personas"),
        tele(contract, "reviewer_models"),
    )
    if not isinstance(personas, list) or not isinstance(models, list):
        return (
            False,
            "the legacy rotation (reviewer_personas, reviewer_models) is not in the contract",
        )
    known = set(classes.values())
    legacy = []
    for p, m in zip(personas, models):
        cls = classes.get(m, str(m).lower())
        if cls not in known:
            return (
                False,
                f"legacy reviewer model {m!r} is neither a mapped model id nor a class name, so parity is not proven",
            )
        legacy.append((str(p), cls))
    if len(legacy) != len(reviewers):
        return False, "the legacy rotation has a different reviewer count"
    if not (resolved == cards == legacy):
        return False, f"resolution {resolved} / cards {cards} / legacy {legacy}"
    return True, ""


def malformed_rows(run: Path) -> int | None:
    """MALFORMED row count of the run's audit.log; None when the file is missing or unreadable."""
    try:
        text = (run / "audit.log").read_text(encoding="utf-8")
    except (OSError, ValueError):
        return None
    return sum(1 for row in text.splitlines() if _MALFORMED.search(row))


def wave4_ev1(run: Path, contract: dict) -> bool | None:
    """True when EV-1 fails, False when it holds, None when Wave 4 did not run (tier 1)."""
    tier = contract.get("tier_reached")
    if isinstance(tier, int) and not isinstance(tier, bool) and tier == 1:
        return None
    return bool(pl.ev1_failures(run, contract, use_manifest=False))


def _rate(flags: list[bool | None]) -> tuple[int, int, float | None]:
    counted = [f for f in flags if f is not None]
    fails = sum(1 for f in counted if f)
    return fails, len(counted), (fails / len(counted) if counted else None)


def collect(runs_root: Path) -> dict:
    """Scan runs_root; returns the per-run records and the legacy baseline."""
    tiers = pnl.load_tiers()
    classes = tiers.get("classes", {})
    tiers_sha256 = pnl.sha256_json(tiers)
    shadow, incomplete, failed = [], [], []
    for mpath in sorted(runs_root.glob("pre-*/panel/manifest.json")):
        run = mpath.parent.parent
        manifest = _json_map(mpath)
        if manifest is None:
            failed.append(f"{run.name} (manifest unreadable)")
            continue
        if manifest.get("t2_engine_effective") != "shadow":
            continue
        state = manifest.get("state")
        if state == "failed":
            failed.append(run.name)
            continue
        if state != "published":
            incomplete.append((run.name, str(state)))
            continue
        contract = _yaml_map(run / "return-contract.yaml") or {}
        parity, why = recompute_parity(run, contract, classes, tiers_sha256)
        recorded = tele(contract, "panel_parity")
        malformed = malformed_rows(run)
        shadow.append(
            {
                "name": run.name,
                "dir": run,
                "manifest_errors": mf.validate(manifest),
                "contract": contract,
                "parity": parity,
                "parity_reason": why,
                "recorded_parity": recorded,
                "wrong_record": recorded is True and not parity,
                "malformed": malformed or 0,
                "audit_unreadable": malformed is None,
                "lint": pl.lint_panel_contract(run, contract)
                if contract
                else ["no contract"],
                "ev1_fail": wave4_ev1(run, contract) if contract else True,
                "shortfall": manifest.get("reviewers_resolved") == 3
                and manifest.get("reviewers_complete") == 2,
                "unknown_executor": tele(contract, "executor_class_resolved") is False,
                "compliance": tele(contract, "findings_block_compliance_rate"),
                "agreement": tele(contract, "cluster_agreement"),
            }
        )
    legacy_dirs, skipped = rv.legacy_runs(runs_root)
    legacy_ev1 = []
    for d in legacy_dirs:
        contract, _ = rv.load(d)
        legacy_ev1.append(wave4_ev1(d, contract) if contract else None)
    return {
        "shadow": shadow,
        "incomplete": incomplete,
        "failed": failed,
        "legacy_dirs": legacy_dirs,
        "legacy_skipped": skipped,
        "legacy_ev1": legacy_ev1,
    }


def replay_diffs(data: dict) -> dict[bool, dict]:
    """Verdict replay of the counted shadow runs against the legacy baseline, per allow_single_vendor value."""
    out = {}
    for allow in rv.SINGLE_VENDOR_MODES:
        legacy = {d.name: v for d in data["legacy_dirs"] if (v := rv.replay(d, allow))}
        shadow = {
            r["name"]: v for r in data["shadow"] if (v := rv.replay(r["dir"], allow))
        }
        out[allow] = rv.compare(legacy, shadow)
    return out


def _fmt(rate: float | None) -> str:
    return "n/a" if rate is None else f"{rate:.3f}"


def build_report(data: dict, required: int) -> tuple[str, str]:
    """(report text, overall verdict)."""
    shadow = data["shadow"]
    failures: list[str] = []
    lines = ["Stage 2 shadow-exit report", ""]
    lines.append(f"shadow runs counted: {len(shadow)} of {required} required")
    for name, state in data["incomplete"]:
        lines.append(f"  incomplete (not counted): {name} (state {state})")
    for name in data["failed"]:
        lines.append(f"  FAILED manifest: {name}")
        failures.append(f"{name}: manifest state failed")

    for r in shadow:
        if r["audit_unreadable"]:
            lines.append(f"  audit.log missing or unreadable: {r['name']}")
            failures.append(f"{r['name']}: audit.log missing or unreadable")
    malformed = sum(r["malformed"] for r in shadow)
    lines.append(f"MALFORMED audit.log rows: {malformed} (must be 0)")
    if malformed:
        failures += [
            f"{r['name']}: {r['malformed']} MALFORMED row(s)"
            for r in shadow
            if r["malformed"]
        ]

    s_fail, s_n, s_rate = _rate([r["ev1_fail"] for r in shadow])
    l_fail, l_n, l_rate = _rate(data["legacy_ev1"])
    lines.append(
        f"EV-1 failure rate (len(reviewer_cards) rule, Wave 4 runs only): shadow {s_fail}/{s_n} = {_fmt(s_rate)}; "
        f"legacy baseline {l_fail}/{l_n} = {_fmt(l_rate)} (must be no higher)"
    )
    if (s_rate or 0.0) > (l_rate or 0.0):
        failures.append("EV-1 failure rate is higher than the legacy baseline")

    lines.append("parity assertion per run (recomputed):")
    for r in shadow:
        note = "" if r["parity"] else f" ({r['parity_reason']})"
        wrong = "; recorded true but recomputed false" if r["wrong_record"] else ""
        lines.append(
            f"  {r['name']}: {'holds' if r['parity'] else 'FAILS'}{note}{wrong}"
        )
        if not r["parity"]:
            failures.append(f"{r['name']}: parity does not hold")

    lines.append("contract lint and manifest per run:")
    for r in shadow:
        problems = r["lint"] + [f"manifest: {e}" for e in r["manifest_errors"]]
        lines.append(
            f"  {r['name']}: {'clean' if not problems else f'{len(problems)} problem(s)'}"
        )
        for p in problems:
            lines.append(f"    {p}")
        if problems:
            failures.append(f"{r['name']}: lint or manifest problems")

    diffs = replay_diffs(data)
    new_degraded = sum(len(d["new_degraded"]) for d in diffs.values())
    lines.append(
        f"verdict replay against the legacy baseline ({len(data['legacy_dirs'])} runs): new degraded reasons {new_degraded}"
    )
    for allow, d in diffs.items():
        for name, reason in d["new_degraded"]:
            lines.append(f"  allow_single_vendor={allow}: {name}: {reason}")
    if new_degraded:
        failures.append("verdict replay found a new degraded reason")

    lines += ["", "Stage 2 counts:"]
    lines.append(f"  2-of-3 shortfalls: {sum(1 for r in shadow if r['shortfall'])}")
    lines.append(
        f"  unknown executor class (executor_class_resolved false): {sum(1 for r in shadow if r['unknown_executor'])}"
    )
    comp = [
        float(r["compliance"])
        for r in shadow
        if isinstance(r["compliance"], (int, float))
        and not isinstance(r["compliance"], bool)
    ]
    lines.append(
        f"  findings-block compliance rate (mean over {len(comp)} run(s)): "
        + (f"{statistics.mean(comp):.3f}" if comp else "n/a")
    )
    agree = [
        float(r["agreement"])
        for r in shadow
        if isinstance(r["agreement"], (int, float))
        and not isinstance(r["agreement"], bool)
    ]
    if agree:
        lines.append(
            f"  cluster_agreement ({len(agree)} run(s)): min {min(agree):.3f}, median {statistics.median(agree):.3f}, max {max(agree):.3f}"
        )
    else:
        lines.append("  cluster_agreement: n/a")

    if failures:
        verdict = "FAIL"
    elif len(shadow) < required:
        verdict = "INSUFFICIENT-RUNS"
    else:
        verdict = "PASS"
    lines += [
        "",
        *[f"failure: {f}" for f in failures],
        f"OVERALL: {verdict} (shadow runs {len(shadow)} of {required})",
    ]
    return "\n".join(lines) + "\n", verdict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs-root", type=Path, default=ROOT / ".dev" / "reflect")
    parser.add_argument("--required", type=int, default=REQUIRED_RUNS)
    parser.add_argument(
        "--out", type=Path, default=None, help="Also write the report to this file."
    )
    args = parser.parse_args(argv)
    if not args.runs_root.is_dir():
        print(f"runs root is not a directory: {args.runs_root}", file=sys.stderr)
        return 2
    report, verdict = build_report(collect(args.runs_root), args.required)
    sys.stdout.write(report)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
