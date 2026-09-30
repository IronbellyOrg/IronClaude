"""Deterministic quantitative metrics (SR, SC) for the two variants."""

import re
from pathlib import Path

D = Path(__file__).parent
VAGUE = re.compile(
    r"\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices)\b",
    re.I,
)
CONCRETE = re.compile(r"[\w./-]+\.(?:md|py):\d+|`[^`]+`|\b\d+\b")
for name in ("variant-1-opus-architect.md", "variant-2-sonnet-refactorer.md"):
    text = D.joinpath(name).read_text(encoding="utf-8")
    body = re.sub(
        r"```.*?```", "", text, flags=re.S
    )  # headings/fences excluded from H2 count
    h2 = len(re.findall(r"^## ", body, re.M))
    c, v = len(CONCRETE.findall(text)), len(VAGUE.findall(text))
    print(f"{name}: concrete={c} vague={v} SR={c / (c + v):.3f} H2={h2}")
