#!/usr/bin/env python3
"""Offline verdict replay of recorded reflect pre contracts (contract compatibility gate, Stage 2 entry check).

Run with ``uv run python scripts/reflect_verdict_replay.py [--runs-root <dir>] [--shadow <run dir> ...]``. It reads
files only: no model, no process, no network, and it writes nothing.

Legacy set: every ``<runs-root>/pre-*`` directory (default runs root: ``.dev/reflect`` under the repository that
holds this script) that holds a ``return-contract.yaml`` which parses to a mapping with ``contract_version`` equal
to the string ``"1.8.0"`` and has no ``panel/manifest.json``. Other contracts are counted and listed as skipped,
with the reason.

Shadow set: the run directories given with ``--shadow`` (a shadow run is one with ``panel/manifest.json``; the
script does not require it, so the legacy runs can be replayed against themselves). With no ``--shadow`` the shadow
set is the legacy set, which is the self-replay: it must report zero differences.

Each contract goes through ``superclaude.cli.reflect.contract.derive_verdict`` with these keyword arguments:
- ``expected_tier=2``: the panel and shadow runs are Tier 2, and the wrapper's T2 gate expects tier 2. A recorded
  Tier 1 run therefore replays as ``degraded-tier1`` on both sides, which is what that gate would say; it is not a
  difference.
- ``allow_single_vendor``: both values are replayed. The flag is an operator opt-in of one run, not a property of
  a recorded contract, and ``derive_verdict`` is first-match-wins: with False a ``single-vendor`` run reports
  ``single-vendor`` and hides any later reason (for example ``adversarial-unavailable``); with True that later
  reason shows. Replaying both, and checking each for new degraded reasons, closes that gap.
- ``child_rc=0``: a recorded contract exists because the audit child finished; an offline replay has no child, so
  the crash and timeout vetoes (rc 124 or non-zero) must not apply.
``promoting`` keeps its default (False): a recorded pre contract is not a promotion run.

Differences: runs are paired by directory name. A paired run differs when its (verdict, reason) differs. A new
degraded reason is a shadow run whose verdict is ``degraded`` and that either (a) is paired with a legacy run whose
(verdict, reason) is not the same, or (b) is unpaired and has a degraded reason that no legacy run has. The script
prints both sets, for each ``allow_single_vendor`` value, and exits 1 when there is any new degraded reason, 0
otherwise, 2 on a usage error. Limits: a shadow contract that is unusable or not 1.8.0 is skipped and listed, and a
shadow verdict of ``blocked`` or ``halted`` is a difference when paired but not a new degraded reason; neither
changes the exit code.

With no ``--shadow`` the legacy run directories are replayed a second time as the shadow set (a self-replay). It
shows that the recorded contracts load and derive the same verdicts on every call; it cannot find a difference.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from superclaude.cli.reflect.contract import derive_verdict

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = "return-contract.yaml"
VERSION = "1.8.0"
DERIVE_ARGS = {"expected_tier": 2, "child_rc": 0}
SINGLE_VENDOR_MODES = (
    False,
    True,
)  # the values of allow_single_vendor that are replayed


def load(run: Path) -> tuple[dict | None, str | None]:
    """(contract mapping, skip reason); the reason is None when the contract is usable."""
    path = run / CONTRACT
    if not path.is_file():
        return None, "no return-contract.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError):
        return None, "unreadable or unparseable"
    if not isinstance(data, dict):
        return None, "not a mapping"
    if data.get("contract_version") != VERSION:
        return None, f"contract_version {data.get('contract_version')!r}"
    return data, None


def replay(run: Path, allow_single_vendor: bool = False) -> tuple[str, str] | None:
    """(verdict, reason) of a usable contract, else None."""
    contract, _ = load(run)
    if contract is None:
        return None
    result = derive_verdict(
        contract, allow_single_vendor=allow_single_vendor, **DERIVE_ARGS
    )
    return result.verdict.value, result.reason


def legacy_runs(runs_root: Path) -> tuple[list[Path], list[tuple[str, str]]]:
    """(legacy run directories, [(name, skip reason)]) under runs_root."""
    runs, skipped = [], []
    for d in sorted(runs_root.glob("pre-*")):
        if not d.is_dir():
            continue
        if (d / "panel" / "manifest.json").exists():
            skipped.append((d.name, "has panel/manifest.json (a shadow run)"))
            continue
        contract, why = load(d)
        if contract is None:
            skipped.append((d.name, why or "unusable"))
        else:
            runs.append(d)
    return runs, skipped


def compare(
    legacy: dict[str, tuple[str, str]], shadow: dict[str, tuple[str, str]]
) -> dict[str, Any]:
    """Differences and new degraded reasons between two {run name: (verdict, reason)} maps."""
    legacy_reasons = {r for v, r in legacy.values() if v == "degraded"}
    changed, new_degraded = [], []
    for name in sorted(shadow):
        got = shadow[name]
        want = legacy.get(name)
        if want is not None and want != got:
            changed.append((name, want, got))
        if got[0] != "degraded":
            continue
        if (want is not None and want != got) or (
            want is None and got[1] not in legacy_reasons
        ):
            new_degraded.append((name, got[1]))
    return {"changed": changed, "new_degraded": new_degraded}


def render(sets: dict, skipped: list, results: dict, self_replay: bool) -> str:
    """sets and results are keyed by the allow_single_vendor value."""

    def tally(side: dict) -> list[str]:
        counts = Counter(f"{v}/{r}" for v, r in side.values())
        return [f"  {n:3d}  {k}" for k, n in sorted(counts.items())]

    first = sets[SINGLE_VENDOR_MODES[0]]
    lines = [
        "Verdict replay (derive_verdict: expected_tier=2, child_rc=0; allow_single_vendor False and True)",
        f"legacy runs replayed: {len(first[0])}; skipped: {len(skipped)}",
        *[f"  skipped {n}: {why}" for n, why in skipped],
        f"shadow runs replayed: {len(first[1])}"
        + (" (self-replay: the legacy set again)" if self_replay else ""),
    ]
    for allow in SINGLE_VENDOR_MODES:
        legacy, shadow = sets[allow]
        result = results[allow]
        lines += [
            f"== allow_single_vendor={allow}",
            "legacy verdict/reason:",
            *tally(legacy),
            "shadow verdict/reason:",
            *tally(shadow),
            f"differences: {len(result['changed'])}",
            *[
                f"  {n}: legacy {w[0]}/{w[1]} -> shadow {g[0]}/{g[1]}"
                for n, w, g in result["changed"]
            ],
            f"new degraded reasons: {len(result['new_degraded'])}",
            *[f"  {n}: {r}" for n, r in result["new_degraded"]],
        ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs-root", type=Path, default=ROOT / ".dev" / "reflect")
    parser.add_argument("--shadow", type=Path, action="append", default=[])
    args = parser.parse_args(argv)
    if not args.runs_root.is_dir():
        print(f"runs root is not a directory: {args.runs_root}", file=sys.stderr)
        return 2
    runs, skipped = legacy_runs(args.runs_root)
    shadow_dirs = args.shadow or runs
    for d in args.shadow:
        if load(d)[0] is None:
            skipped.append((d.name, f"shadow: {load(d)[1] or 'unusable'}"))
    sets, results = {}, {}
    for allow in SINGLE_VENDOR_MODES:
        legacy = {d.name: v for d in runs if (v := replay(d, allow)) is not None}
        shadow = {d.name: v for d in shadow_dirs if (v := replay(d, allow)) is not None}
        sets[allow], results[allow] = (legacy, shadow), compare(legacy, shadow)
    sys.stdout.write(render(sets, skipped, results, not args.shadow))
    return 1 if any(r["new_degraded"] for r in results.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
