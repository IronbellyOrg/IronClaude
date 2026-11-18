"""Step 08 evaluation: judge answers (5 runs x 3 batches) -> verdicts -> agreement with the panel consensus.
Run from anywhere: uv run python evaluate.py
Writes results.md next to this file. Fallback-judge run (an LLM, not Jev).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "07-classifier"))
from truth_table import classify  # noqa: E402

# panel consensus: mean of the three blind scorers >= 4.0 is a blocker
scores = {}
for n in (1, 2, 3):
    for line in (ROOT / "05-scoring" / f"scores-{n}.md").read_text().splitlines():
        m = re.match(r"^(F-B\d\d-\d+) \| ([1-5])$", line.strip())
        if m:
            scores.setdefault(m[1], []).append(int(m[2]))
truth = {k: sum(v) / 3 >= 4 for k, v in scores.items()}
mean = {k: sum(v) / 3 for k, v in scores.items()}
assert len(truth) == 318 and all(len(v) == 3 for v in scores.values())

runs = {}
problems = []
for r in range(1, 6):
    res = {}
    for b in (1, 2, 3):
        f = HERE / "answers" / f"run{r}-batch{b}.jsonl"
        if not f.exists():
            problems.append(f"missing {f.name}")
            continue
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                p = json.loads(line)
                st, v, c = classify(p)
                res[p["id"]] = (v, c)
            except Exception as e:  # keep going, report
                problems.append(f"{f.name}:{i} {e}")
    runs[r] = res


def metrics(res, show_as):
    """show_as: 'blocker' or 'not' - how a SHOW_USER verdict is counted."""
    tp = fp = fn = tn = 0
    for k, t in truth.items():
        if k not in res:
            continue
        v = res[k][0]
        pred = v == "BLOCKING" or (v == "SHOW_USER" and show_as == "blocker")
        tp += pred and t
        fp += pred and not t
        fn += (not pred) and t
        tn += (not pred) and not t
    n = tp + fp + fn + tn
    return dict(n=n, tp=tp, fp=fp, fn=fn, tn=tn,
                acc=(tp + tn) / n if n else 0,
                prec=tp / (tp + fp) if tp + fp else 0,
                rec=tp / (tp + fn) if tp + fn else 0)


out = ["# Step 08 results: fallback LLM judge, five runs (not a Jev run)", ""]
if problems:
    out += ["Problems: " + "; ".join(problems[:10]), ""]
out += ["Truth: panel mean >= 4.0 (82 blockers of 318). Status-quo baseline (every finding was filed as blocking): precision 25.8%, recall 100%.", "",
        "| Run | Rows | BLOCKING | SHOW_USER | FOLLOW_UP | NOTE | Accuracy (SHOW_USER = not blocker) | Precision | Recall | Accuracy (SHOW_USER = blocker) | Precision | Recall |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for r, res in runs.items():
    cnt = Counter(v for v, _ in res.values())
    a, b = metrics(res, "not"), metrics(res, "blocker")
    out.append(f"| {r} | {len(res)} | {cnt['BLOCKING']} | {cnt['SHOW_USER']} | {cnt['FOLLOW_UP']} | {cnt['NOTE']} | "
               f"{a['acc']:.1%} | {a['prec']:.1%} | {a['rec']:.1%} | {b['acc']:.1%} | {b['prec']:.1%} | {b['rec']:.1%} |")

complete = [k for k in truth if all(k in runs[r] for r in runs)]
flip = [k for k in complete if len({runs[r][k][0] == "BLOCKING" for r in runs}) > 1]
maj = {k: sum(runs[r][k][0] == "BLOCKING" for r in runs) >= 3 for k in complete}
tp = sum(maj[k] and truth[k] for k in complete)
fp = sum(maj[k] and not truth[k] for k in complete)
fn = sum((not maj[k]) and truth[k] for k in complete)
tn = sum((not maj[k]) and not truth[k] for k in complete)
out += ["", f"Findings answered in all five runs: {len(complete)}. Findings whose blocker call flips between runs: {len(flip)} ({len(flip)/max(1,len(complete)):.1%}).",
        "", "Majority of five runs (BLOCKING in 3 or more runs) against the panel:", "",
        "| | Panel blocker | Panel not blocker |", "|---|---|---|",
        f"| Judge blocker | {tp} | {fp} |", f"| Judge not blocker | {fn} | {tn} |", "",
        f"Majority accuracy {(tp+tn)/max(1,len(complete)):.1%}, precision {tp/max(1,tp+fp):.1%}, recall {tp/max(1,tp+fn):.1%}.", ""]

# confidence calibration on BLOCKING verdicts, pooled over runs
bins = {}
for r, res in runs.items():
    for k, (v, c) in res.items():
        if v == "BLOCKING" and c is not None and k in truth:
            b = min(int(c * 10), 9)
            bins.setdefault(b, [0, 0])
            bins[b][0] += 1
            bins[b][1] += truth[k]
out += ["BLOCKING verdicts by confidence (pooled over runs): how often the panel agreed", "", "| Confidence bin | Verdicts | Panel agreed |", "|---|---|---|"]
for b in sorted(bins):
    n, a = bins[b]
    out.append(f"| {b/10:.1f}-{(b+1)/10:.1f} | {n} | {a} ({a/n:.0%}) |")

# disagreements to inspect: high-consensus rows the majority got wrong
miss = sorted((k for k in complete if maj[k] != truth[k]), key=lambda k: -abs(mean[k] - 3.5))[:15]
out += ["", "Largest disagreements (panel mean in brackets):", ""]
out += [f"- {k} [{mean[k]:.2f}] panel {'blocker' if truth[k] else 'not blocker'}, judge majority {'blocker' if maj[k] else 'not blocker'}" for k in miss]
(HERE / "results.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
