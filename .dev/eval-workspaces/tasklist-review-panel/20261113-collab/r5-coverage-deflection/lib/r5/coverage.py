"""Findings -> covered Tasks, surface filter, declared not-checked Tasks, ranking and card contents (DESIGN 2.3)."""
import hashlib
import re

from superclaude.cli.review.findings import locate

from r5 import cfg

TASK_HEAD = re.compile(r"^## Task (\d+):")
ANY_H2 = re.compile(r"^## ")
REF_TASK = re.compile(r"\bTask\s+(\d+)\b", re.I)
NOTCHK = re.compile(
    r"\b(did not|didn't|not (?:check|checked|verify|verified|review|reviewed|inspect|inspected|"
    r"validate|validated|cover|covered)|unchecked|unverified|skipped|out of scope)\b",
    re.I,
)
TASK_LIST = re.compile(r"\bTasks?\s+(\d+(?:\s*(?:-|–|to|,|and|&|or)\s*\d+)*)", re.I)
NUM_OR_RANGE = re.compile(r"(\d+)\s*(?:-|–|to)\s*(\d+)|(\d+)")
FINDINGS_FENCE = re.compile(r"^\s{0,3}```findings-v1.*?^\s{0,3}```[ \t]*$", re.S | re.M)


def surface_pattern() -> str:
    return (cfg() / "surface.regex").read_text().strip()


def task_index(candidate_text: str) -> list[tuple[str, int, int]]:
    """(Task id, first line, end line) with 0-based half-open line ranges ending at the next '## ' heading."""
    lines = candidate_text.splitlines()
    out = []
    for i, line in enumerate(lines):
        m = TASK_HEAD.match(line)
        if not m:
            continue
        end = next((j for j in range(i + 1, len(lines)) if ANY_H2.match(lines[j])), len(lines))
        out.append((f"T{m.group(1)}", i, end))
    return out


def tasks_of(finding: dict, candidate_text: str, index) -> set[str]:
    hit: set[str] = set()
    located = False
    for key in ("anchor", "anchor2"):
        a = finding.get(key)
        if not isinstance(a, str) or not a.strip():
            continue
        for start, _end in locate(candidate_text, a):
            located = True
            hit |= {tid for tid, s, e in index if s <= start < e}
    if not located:
        known = {tid for tid, _s, _e in index}
        for r in finding.get("refs") or []:
            if isinstance(r, str):
                hit |= {f"T{n}" for n in REF_TASK.findall(r)} & known
    return hit


def is_surface(finding: dict, pattern: str) -> bool:
    return bool(re.search(pattern, finding.get("claim") or "", re.I))


def covered(findings, candidate_text: str, index, pattern: str) -> set[str]:
    out: set[str] = set()
    for f in findings:
        if not is_surface(f, pattern):
            out |= tasks_of(f, candidate_text, index)
    return out


def _task_numbers(listing: str) -> set[str]:
    out = set()
    for m in NUM_OR_RANGE.finditer(listing):
        if m.group(3):
            out.add(f"T{int(m.group(3))}")
        else:
            a, b = int(m.group(1)), int(m.group(2))
            if a <= b <= a + 50:
                out |= {f"T{n}" for n in range(a, b + 1)}
    return out


def declared_not_checked(report_text: str) -> set[str]:
    text = FINDINGS_FENCE.sub(" ", report_text)
    out: set[str] = set()
    for sentence in re.split(r"(?<=[.!?])\s+|\n+", text):
        if NOTCHK.search(sentence):
            for m in TASK_LIST.finditer(sentence):
                out |= _task_numbers(m.group(1))
    return out


def tie_key(row: str, pkg: str, tid: str) -> str:
    return hashlib.sha256(f"{row}/{pkg}/{tid}".encode()).hexdigest()


def rank(uncovered, declared: dict, row: str, pkg: str) -> list[str]:
    """Declared-not-checked uncovered Tasks first (more scouts naming it first), then the sha256 tie-break (D4)."""
    return sorted(uncovered, key=lambda t: (-declared.get(t, 0), tie_key(row, pkg, t)))


def next_card(prev: dict, rank_list: list, uncovered: set, k: int, receivers: list, deal_r: int) -> dict:
    """Per receiver: (items or None, status). prev maps receiver -> items of its last posted card.

    Rank position i goes to receiver (i + deal_r) mod n (n = 1 for single-receiver panels).
    A replacing card keeps the receiver's still-uncovered Tasks, then fills from its share up to k (D3).
    """
    n = len(receivers)
    out = {}
    for idx, rid in enumerate(receivers):
        if k <= 0:
            out[rid] = (None, "k0")
            continue
        share = [t for i, t in enumerate(rank_list) if (i + deal_r) % n == idx]
        old = prev.get(rid)
        if old is None:
            items = share[:k]
        else:
            items = [t for t in old if t in uncovered]
            for t in share:
                if len(items) >= k:
                    break
                if t not in items:
                    items.append(t)
            if items and set(items) == set(old):
                out[rid] = (None, "dup_card")
                continue
        out[rid] = (items, "post") if items else (None, "nothing_uncovered")
    return out


def render_card(items: list, k: int, second: bool) -> str:
    """Same rendering as bin/hook-posttool.sh (the audit re-runs it to check the delivered text sha)."""
    tpl = (cfg() / "templates" / ("card-2.txt" if second else "card-1.txt")).read_text()
    tasks = ", ".join(f"Task {t[1:]}" for t in items)
    return tpl.replace("{TASKS}", tasks).replace("{K}", str(k))
