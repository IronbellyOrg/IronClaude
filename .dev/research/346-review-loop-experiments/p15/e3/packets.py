"""E3 packet builder and code-owned checks (plan 2.1).  Pure functions; no network, no Jev.

build_packet(candidate_text, finding_section) -> Packet
  - strips severity words and reviewer reasoning lines (as p12/ab2 DROP_LINE) from what Jev sees,
  - extracts the claim (`finding.wrong_outcome`: the grading sentence, else the heading),
  - extracts quoted texts (backticked or double-quoted spans of >= 12 characters), checks each verbatim against the candidate,
  - keeps up to 2 found texts (distinct lines) as e1, e2 with their line number and +-3 lines of context.
Code-owned outcomes (no Jev call): EXCEPTION (CRITICAL label, or id FR-8/FR-9) -> RETAIN; QUOTE_FAIL (no quoted span found
verbatim) -> VERIFIER.  S:NN citations only choose which occurrence of a repeated quote is the evidence line."""
import re
from dataclasses import dataclass, field

import e3lib

MIN_QUOTE = 12
CONTEXT = 3
SEV_WORDS = r"CRITICAL|MAJOR|MINOR|MEDIUM|non-blocking|not blocking|blocking"
DROP_LINE = re.compile(r"(?i)^\s*(?:[-*]\s*)?(?:\*\*)?\s*(recommendation|rationale|experts?|priority|quality impact|why blocking|suggested fix)\b")
SEV_ANY = re.compile(r"(?i)\b(?:" + SEV_WORDS + r")\b")
_PAREN_SEV = re.compile(r"(?i)\(\s*(?:(?:" + SEV_WORDS + r"|graded|and|FR-\d+|,|\.|;|\s)+)\s*\)")
_SEV_LABEL = re.compile(r"(?i)\bSeverity\b\s*:?")
_EXPERT = re.compile(r"\bExperts?\s*:\s*.*?\.(?=\s+[A-Z`*])")
_ID_PREFIX = re.compile(r"^\W*(?:R\d-)?[A-Z]{1,4}-?\d+(?:-\d+)?\b\s*[.:)\-]?\s*")
_GRADING = re.compile(r"(?is)\b(an implementer who follows\b.*?)(?=\n\s*\n|\n\s*[-*]\s|\Z)")
_CRIT_RX = None


def strip_severity(s: str) -> str:
    """Remove severity words (CRITICAL|MAJOR|MINOR|MEDIUM|blocking|...) and tidy the punctuation they leave."""
    s = _PAREN_SEV.sub(" ", s)
    s = _SEV_LABEL.sub(" ", s)
    s = SEV_ANY.sub(" ", s)
    s = re.sub(r"\(\s*[,;.\s]*\)", " ", s)
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = re.sub(r"([,;:])(\s*[,;:])+", r"\1", s)
    s = re.sub(r"^[\s,;:.\-]+", "", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def _clean_markup(s: str) -> str:
    s = re.sub(r"^\s*#{1,6}\s*", "", s)
    s = re.sub(r"^\s*[-*]\s+", "", s)
    return s.replace("**", "").strip()


def clean_title(heading: str) -> str:
    h = _clean_markup(heading)
    h = _ID_PREFIX.sub("", h, count=1)
    h = _EXPERT.sub("", h)
    return strip_severity(h)


def drop_reasoning(section: str) -> str:
    lines = [ln for ln in section.splitlines() if not DROP_LINE.match(ln)]
    return "\n".join(lines)


def extract_claim(section: str, title: str) -> str:
    m = _GRADING.search(section)
    if m:
        c = re.sub(r"\s+", " ", m.group(1)).strip()
        c = strip_severity(c)
        if len(c) > 1200:
            c = c[:1200].rsplit(" ", 1)[0]
        if c:
            return c
    return title


def extract_quotes(text: str) -> list:
    """Backticked and double-quoted spans of >= MIN_QUOTE characters, in order of appearance, de-duplicated."""
    spans = []
    for m in re.finditer(r"`([^`\n]{%d,})`|\"([^\"\n]{%d,})\"|“([^”\n]{%d,})”" % (MIN_QUOTE, MIN_QUOTE, MIN_QUOTE), text):
        q = next(g for g in m.groups() if g is not None)
        spans.append((m.start(), q.strip()))
    spans.sort()
    out = []
    for _, q in spans:
        if len(q) >= MIN_QUOTE and q not in out:
            out.append(q)
    return out


def cited_lines(text: str) -> list:
    """Line numbers cited as `spec:NN`, `S:NN` or `line NN` (ranges expanded, order of appearance)."""
    out = []
    for m in re.finditer(r"(?i)(?:\b(?:spec|S)\s*:\s*|\blines?\s+)(\d{1,3})(?:\s*[-–]\s*(\d{1,3}))?", text):
        a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
        out.extend(range(a, b + 1) if 0 <= b - a <= 30 else [a])
    return out


def _lines_of(candidate: str, text: str):
    """1-based line numbers where `text` starts (single-line texts) in candidate."""
    first = candidate.find(text)
    res = []
    while first != -1:
        res.append(candidate.count("\n", 0, first) + 1)
        first = candidate.find(text, first + 1)
    return res


def _context(candidate_lines: list, line: int) -> str:
    lo, hi = max(1, line - CONTEXT), min(len(candidate_lines), line + CONTEXT)
    return "\n".join(candidate_lines[lo - 1:hi])


def is_exception(heading: str, section: str = "", finding_id=None, dec=None) -> bool:
    """Code-owned canonical exception: the finding's label is CRITICAL (heading/label line) or its id is FR-8/FR-9."""
    global _CRIT_RX
    d = dec or e3lib.decision()
    if _CRIT_RX is None:
        _CRIT_RX = re.compile(d["exceptions"]["label_regex"])
    ids = set(d["exceptions"]["ids"])
    if finding_id and finding_id in ids:
        return True
    head = _clean_markup(heading)
    if re.match(r"^\W*(?:" + "|".join(re.escape(i) for i in ids) + r")(?![\w-])", head):
        return True
    if _CRIT_RX.search(heading or ""):
        return True
    # a label line below the heading ("- Severity: CRITICAL ...") is the same label
    return bool(re.search(r"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?(?:severity|label|grade)\b[^\n]*" + _CRIT_RX.pattern.replace("(?i)", ""), section or ""))


@dataclass
class Packet:
    code_outcome: str                 # "OK" | "EXCEPTION" | "QUOTE_FAIL"
    reason: str
    title: str = ""
    claim: str = ""
    evidence: dict = field(default_factory=dict)      # {"e1": {"text", "line", "context"}, "e2": {...}}
    quotes_extracted: int = 0
    quotes_found: int = 0
    state: dict = None                # the Jev state when code_outcome == "OK"

    @property
    def evidence_count(self):
        return len(self.evidence)

    def to_dict(self):
        return {"code_outcome": self.code_outcome, "reason": self.reason, "title": self.title, "claim": self.claim,
                "evidence": self.evidence, "quotes_extracted": self.quotes_extracted, "quotes_found": self.quotes_found,
                "state": self.state}


def state_of(title: str, claim: str, evidence: dict) -> dict:
    return {"finding": {"title": title, "wrong_outcome": claim},
            "evidence": evidence,
            "facts": {"quotes_found_verbatim": True, "evidence_count": len(evidence)}}


def build_packet(candidate_text: str, finding_section: str, finding_id=None, dec=None) -> Packet:
    sec = finding_section.strip("\n")
    first_line = next((ln for ln in sec.splitlines() if ln.strip()), "")
    title = clean_title(first_line)
    body = drop_reasoning(sec)
    if is_exception(first_line, sec, finding_id, dec):
        return Packet("EXCEPTION", "CRITICAL label or FR-8/FR-9 id: retained by code, never sent to Jev or the verifier", title=title)
    claim = extract_claim(body, title)
    quotes = extract_quotes(body)
    cites = cited_lines(body)
    clines = candidate_text.splitlines()
    found = []
    for q in quotes:
        if q not in candidate_text:
            continue
        lines = _lines_of(candidate_text, q)
        line = next((l for l in lines if l in cites), lines[0])
        found.append((q, line))
    if not found:
        return Packet("QUOTE_FAIL", "no quoted text found verbatim in the candidate", title=title, claim=claim,
                      quotes_extracted=len(quotes), quotes_found=0)
    ev, used = {}, []
    for q, line in found:
        if any(line == l for _, l in used) or any(q in u or u in q for u, _ in used):
            continue
        used.append((q, line))
        if len(used) == 2:
            break
    for i, (q, line) in enumerate(used, start=1):
        ev[f"e{i}"] = {"text": q, "line": line, "context": _context(clines, line)}
    p = Packet("OK", "ok", title=title, claim=claim, evidence=ev, quotes_extracted=len(quotes), quotes_found=len(found))
    p.state = state_of(title, claim, ev)
    return p


def packet_of_case(case: dict, dec=None) -> Packet:
    """Packet of a J8 case file: perturbation cases carry their final Jev `state` (and code outcome); every other case is built
    from its candidate text and finding section."""
    pk = case["packet"]
    if "state" in pk:
        st = pk["state"]
        ev = st["evidence"]
        return Packet(pk.get("code_outcome", "OK"), "perturbed packet", title=st["finding"]["title"],
                      claim=st["finding"]["wrong_outcome"], evidence=ev, quotes_extracted=len(ev), quotes_found=len(ev), state=st)
    return build_packet(e3lib.candidate_of(case), pk["finding_section"], finding_id=pk.get("finding_id"), dec=dec)
