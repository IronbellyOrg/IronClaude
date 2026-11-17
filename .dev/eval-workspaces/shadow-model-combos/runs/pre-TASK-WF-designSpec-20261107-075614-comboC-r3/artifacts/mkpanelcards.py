"""Step 5 (shadow): write panel/cards/reviewer-<N>.md after calibration. Run: uv run python mkpanelcards.py <output_dir>"""
import os
import re
import sys

out = sys.argv[1]
os.makedirs(f"{out}/panel/cards", exist_ok=True)
PER_FINDING = {
    1: {"F1": 0.85, "F2": 0.85, "F3": 0.80},
    2: {"F1": 0.85, "F2": 0.75, "F3": 0.80, "F4": 0.90, "F5": 0.80},
    3: {"F1": 0.85, "F2": 0.60, "F3": 0.65, "F4": 0.70, "F5": 0.75, "F6": 0.70},
}
for n in (1, 2, 3):
    text = open(f"{out}/reviewer-cards/reviewer-{n}-card.md", encoding="utf-8").read()
    head = text.split("\n\n", 1)[0]  # persona / model_class / model lines
    assert head.count("\n") == 2, head
    m = re.search(r"^## Findings block\n\n```findings-v2\n.*?\n```\n", text, re.S | re.M)
    assert m, n
    sr = re.search(r"^reviewer_model_self_report:.*$", text, re.M).group(0)
    cal = "calibration:\n  per_finding:\n" + "".join(f"    {k}: {v}\n" for k, v in PER_FINDING[n].items())
    body = f"{head}\n\n{m.group(0)}\n{sr}\n\n```yaml\n{cal}```\n"
    open(f"{out}/panel/cards/reviewer-{n}.md", "w", encoding="utf-8").write(body)
    print(n, "written", len(body), "bytes")
