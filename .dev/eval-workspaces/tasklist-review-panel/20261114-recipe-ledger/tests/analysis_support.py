"""Shared setup of the analysis tests (Task 15): the F-RUNS-RL fixture built once per session and analysed once.

fixture(factory, variant="base") -> SimpleNamespace(fx, runs, by_id, scores, gt, metrics, rows)
Each test module wraps it in a one-line pytest fixture, because the copied conftest.py is not edited.
"""

from types import SimpleNamespace

from analysis import analyze as az
from fixtures.runs import make_runs as mr

_CACHE = {}


def fixture(factory, variant="base"):
    if variant not in _CACHE:
        fx = mr.build(factory.mktemp(f"runs-{variant}"), variant)
        runs = az.load_runs(fx.runs, "stage1-")
        scores, bad = az.load_scores(fx.scoring)
        assert not bad and len(scores) == 40
        gt = az.load_gt(fx.gt)
        metrics, rows = az.analyse(runs, gt, scores, 1, {}, az.SEED, az.BOOT_N)
        _CACHE[variant] = SimpleNamespace(
            fx=fx,
            runs=runs,
            by_id={r["id"]: r for r in runs},
            scores=scores,
            gt=gt,
            metrics=metrics,
            rows=rows,
        )
    return _CACHE[variant]
