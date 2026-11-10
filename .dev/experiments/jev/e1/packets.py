"""Packet builder of plan section 2.1.  Code owns identity, cited lines, grading sentence, obligation, mapped hunks, verbatim flags,
tombstones, dependency retrieval and the prechecks.  No reviewer or reviser assertion ever enters the state (the revise report is not an input)."""
import _boot  # noqa: F401
import difflib
import hashlib
import re
from dataclasses import asdict, dataclass, field

import score_themes as ST
from jevlib import config as C
from jevlib.questions import build_request, canonical_bytes
from questions import MAX_DEPS, questions_for

CONTEXT = 3
GRADING_RX = re.compile(r"An implementer who follows .*? builds .*?(?:\.|$)", re.S)
PROTECTED_RX = re.compile(r"(?im)^\W*(?:protected requirement|must hold)\b[^:\n]*:\s*(.+)$")
CONTRADICT_RX = re.compile(r"(?i)contradict|conflict|inconsisten")
ID_RX = re.compile(r"\b[A-Z]{1,4}-\d+(?:\.\d+)?\b")
BACKTICK_RX = re.compile(r"`([^`\n]+)`")
SECTION_REF_RX = re.compile(r"(?i)(?:\bsections?|§)\s*(\d+(?:\.\d+)*)")
PRECHECKS = ("ok", "noop", "regressed", "stale", "unmapped", "deps", "oversize")


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


@dataclass
class Packet:
    packet_id: str
    run: str
    review: str
    finding_id: str
    before_sha: str
    after_sha: str
    precheck: str
    reason: str
    cited: list
    defect_lines: list
    obligation_lines: list
    obligation_text: str
    obligation_where: str
    summary: str
    wrong_outcome: str
    before_passage: str
    after_passage: str
    diff: str
    mapped_hunks: int
    obligation_still_verbatim: bool
    defect_still_verbatim: bool
    tombstones: list
    dependencies: dict          # {"d1": {"text", "where"}}
    n_deps_needed: int
    unresolved_refs: list
    previously_closed: bool
    est_tokens: int = 0

    def to_dict(self):
        return asdict(self)

    @property
    def eligible(self) -> bool:
        """Eligible for a Jev call / a conventional check: only precheck 'ok'."""
        return self.precheck == "ok"

    @property
    def n_deps(self) -> int:
        return len(self.dependencies)


# ---------------------------------------------------------------- helpers
def _clean_heading(h: str) -> str:
    return re.sub(r"^[\s#*]+|[\s*]+$", "", h or "").strip()


def _ranges(nums):
    out, nums = [], sorted(set(nums))
    for n in nums:
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return out


def _where(side: str, nums) -> str:
    rs = _ranges(nums)
    word = "line" if len(rs) == 1 and rs[0][0] == rs[0][1] else "lines"
    return f"{side}, {word} " + ", ".join(f"{a}-{b}" if a != b else f"{a}" for a, b in rs)


def _window(nums, n_lines, ctx=CONTEXT):
    """Merged 1-based inclusive windows around `nums`, +-ctx lines."""
    out = []
    for n in sorted(set(nums)):
        a, b = max(1, n - ctx), min(n_lines, n + ctx)
        if out and a <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def _join_windows(lines, wins):
    return "\n...\n".join("\n".join(lines[a - 1:b]).strip("\n") for a, b in wins)


def grading_sentence(finding_text: str, heading: str) -> str:
    m = GRADING_RX.search(finding_text or "")
    return re.sub(r"\s+", " ", m.group(0)).strip() if m else _clean_heading(heading)


def _is_content(line: str) -> bool:
    s = line.strip()
    return bool(s) and not s.startswith("#")


def split_finding(before_lines, heading, body):
    """-> (cited, defect, obligation) as sorted 1-based line lists resolved against the BEFORE text."""
    n = len(before_lines)
    cited = sorted(x for x in ST.cited((heading or "") + "\n" + (body or "")) if 1 <= x <= n and _is_content(before_lines[x - 1]))
    if not cited:
        return [], [], []
    m = PROTECTED_RX.search(body or "")
    prot = sorted(x for x in (ST.cited(m.group(1)) if m else set()) if x in cited)
    if prot:
        oblig = prot
        defect = [x for x in cited if x not in prot] or cited
    elif CONTRADICT_RX.search(body or "") and len(cited) >= 2:
        oblig, defect = [cited[0]], cited[1:]
    else:
        oblig, defect = cited, cited
    return cited, defect, oblig


# ---------------------------------------------------------------- hunks
def _hunks(before_lines, after_lines):
    sm = difflib.SequenceMatcher(None, before_lines, after_lines, autojunk=False)
    out = []
    for g in sm.get_grouped_opcodes(CONTEXT):
        chg_b, chg_a, bt, at, diff = set(), set(), [], [], []
        for tag, i1, i2, j1, j2 in g:
            if tag == "equal":
                diff += [" " + x for x in before_lines[i1:i2]]
                continue
            diff += ["-" + x for x in before_lines[i1:i2]] + ["+" + x for x in after_lines[j1:j2]]
            bt += before_lines[i1:i2]
            at += after_lines[j1:j2]
            if i1 == i2:                       # pure insertion: it touches the lines on both sides of the insertion point
                chg_b.update({i1, i1 + 1})
            chg_b.update(range(i1 + 1, i2 + 1))
            chg_a.update(range(j1 + 1, j2 + 1))
        i_a, i_b, j_a, j_b = g[0][1], g[-1][2], g[0][3], g[-1][4]
        out.append({"before_range": (i_a + 1, i_b), "after_range": (j_a + 1, j_b), "changed_before": chg_b, "changed_after": chg_a,
                    "before_text": bt, "after_text": at,
                    "diff": f"@@ -{i_a + 1},{i_b - i_a} +{j_a + 1},{j_b - j_a} @@\n" + "\n".join(diff)})
    return out


def _ws_only(h) -> bool:
    squash = lambda xs: re.sub(r"\s+", "", "".join(xs))   # `diff -w` semantics, also across re-wrapped lines
    return squash(h["before_text"]) == squash(h["after_text"])


def _tokens(obligation_text):
    return set(ID_RX.findall(obligation_text)) | set(BACKTICK_RX.findall(obligation_text))


# ---------------------------------------------------------------- dependencies
def _def_rx(ident):
    return re.compile(r"^\s*(?:[-*]|\d+\.)?\s*\**\s*" + re.escape(ident) + r"(?![\w-]|\.\d)")


def _in_wins(i, wins):   # i 1-based
    return any(a <= i <= b for a, b in wins)


def _block(lines, start, cap=8):
    """The definition line plus its continuation (until a blank line, a list item or a heading)."""
    out = [lines[start]]
    for ln in lines[start + 1:start + cap]:
        if not ln.strip() or re.match(r"^\s*(?:[-*]|\d+\.)\s", ln) or ln.lstrip().startswith("#"):
            break
        out.append(ln)
    return "\n".join(out)


def _section(lines, start, cap=15):
    level = len(re.match(r"^\s*(#+)", lines[start]).group(1))
    out = [lines[start]]
    for ln in lines[start + 1:start + cap]:
        m = re.match(r"^\s*(#+)\s", ln)
        if m and len(m.group(1)) <= level:
            break
        out.append(ln)
    return "\n".join(out).rstrip()


def find_dependencies(after_lines, passage_text, wins):
    """Passages of the AFTER text that the after passage refers to by id or section number and that are defined outside it.
    -> (list of {"text","where"} in order of first reference, unresolved refs).  Exact retrieval, never a model."""
    deps, unresolved, seen = [], [], set()
    pass_lines = passage_text.split("\n")
    refs = []   # (position, kind, ident)
    for m in ID_RX.finditer(passage_text):
        refs.append((m.start(), "id", m.group(0)))
    for m in SECTION_REF_RX.finditer(passage_text):
        refs.append((m.start(), "section", m.group(1)))
    for _, kind, ident in sorted(refs):
        if (kind, ident) in seen:
            continue
        seen.add((kind, ident))
        if kind == "id":
            rx = _def_rx(ident)
            if any(rx.match(ln) for ln in pass_lines):
                continue                       # defined inside the passage itself
            idx = next((i for i, ln in enumerate(after_lines) if rx.match(ln) and not _in_wins(i + 1, wins)), None)
            if idx is None:
                unresolved.append(ident); continue
            deps.append({"text": _block(after_lines, idx), "where": ident})
        else:
            rx = re.compile(r"^\s*#{1,6}\s*(?:\*\*)?" + re.escape(ident) + r"(?![\d])")
            if any(rx.match(ln) for ln in pass_lines):
                continue
            idx = next((i for i, ln in enumerate(after_lines) if rx.match(ln) and not _in_wins(i + 1, wins)), None)
            if idx is None:
                unresolved.append(f"section {ident}"); continue
            deps.append({"text": _section(after_lines, idx), "where": f"section {ident}"})
    return deps, unresolved


# ---------------------------------------------------------------- state
def packet_state(p: Packet) -> dict:
    """The one Jev state of a packet (field names fixed by plan 2.1).  Only code-derived facts; no reviewer/reviser assertion."""
    return {"obligation": {"text": p.obligation_text, "where": p.obligation_where},
            "defect": {"summary": p.summary, "wrong_outcome": p.wrong_outcome},
            "before": {"passage": p.before_passage},
            "after": {"passage": p.after_passage, "obligation_text_still_verbatim": p.obligation_still_verbatim,
                      "defect_text_still_verbatim": p.defect_still_verbatim},
            "diff": p.diff,
            "dependencies": {k: {"text": v["text"], "where": v["where"]} for k, v in p.dependencies.items()}}


def oversize(state: dict, n_deps: int) -> bool:
    """Contract J1.6 limits, applied locally (never truncation)."""
    req = build_request(state, questions_for(n_deps))
    if len(canonical_bytes(req)) / C.SIZE_BYTES_PER_TOKEN > C.LIMIT_REQUEST_TOKENS:
        return True
    sb = len(canonical_bytes(req["state"]))
    return any((sb + len(canonical_bytes(q))) / C.SIZE_BYTES_PER_TOKEN > C.LIMIT_QUESTION_TOKENS for q in req["questions"].values())


# ---------------------------------------------------------------- build
def build_packet(before_text: str, after_text: str, finding: dict, history: dict = None) -> Packet:
    """finding: {"run","review","id","heading","body"}; history: {"previously_closed": bool, "recorded_before_sha": str|None, ...}.
    Anything else in `history` (and any revise-report text) is ignored by construction."""
    history = history or {}
    run, review, fid = str(finding.get("run", "")), str(finding.get("review", "")), str(finding["id"])
    heading, body = finding.get("heading") or "", finding.get("body") or ""
    before_lines, after_lines = before_text.splitlines(), after_text.splitlines()
    b_sha, a_sha = sha256_text(before_text), sha256_text(after_text)
    cited, defect, oblig = split_finding(before_lines, heading, body)
    prev = bool(history.get("previously_closed"))
    base = dict(packet_id=finding.get("packet_id") or f"{run}/{review}/{fid}", run=run, review=review, finding_id=fid,
                before_sha=b_sha, after_sha=a_sha, cited=cited, defect_lines=defect, obligation_lines=oblig,
                summary=_clean_heading(heading), wrong_outcome=grading_sentence(heading + "\n" + body, heading),
                previously_closed=prev, mapped_hunks=0, diff="", before_passage="", after_passage="", obligation_text="",
                obligation_where="", obligation_still_verbatim=False, defect_still_verbatim=False, tombstones=[],
                dependencies={}, n_deps_needed=0, unresolved_refs=[])

    def done(precheck, reason, **kw):
        d = {**base, **kw, "precheck": precheck, "reason": reason}
        return Packet(**d)

    rec = history.get("recorded_before_sha")
    if rec and rec != b_sha:
        return done("stale", "before text sha differs from the recorded spec version")
    if not cited:
        return done("unmapped", "no cited line resolves in the before text")

    oblig_text = "\n".join(before_lines[n - 1] for n in oblig)
    after_set = after_text
    ob_verb = all(before_lines[n - 1].strip() in after_set for n in oblig)
    defect_content = [before_lines[n - 1].strip() for n in defect if _is_content(before_lines[n - 1])]
    df_verb = any(t in after_set for t in defect_content)
    tomb = [{"line": n, "text": before_lines[n - 1]} for n in cited if before_lines[n - 1].strip() not in after_set]
    facts = dict(obligation_text=oblig_text, obligation_where=_where("before", oblig),
                 obligation_still_verbatim=ob_verb, defect_still_verbatim=df_verb, tombstones=tomb,
                 before_passage=_join_windows(before_lines, _window(cited, len(before_lines))))

    if prev and df_verb:
        return done("regressed", "a previously closed finding whose defect text is still present verbatim", **facts)

    # mapped hunks
    toks = _tokens(oblig_text)
    cited_set = set(cited)
    cited_texts = [before_lines[n - 1].strip() for n in cited if _is_content(before_lines[n - 1])]
    mapped = []
    for h in _hunks(before_lines, after_lines):
        chg_text = "\n".join(h["before_text"] + h["after_text"])
        added = "\n".join(h["after_text"])
        if (h["changed_before"] & cited_set) or any(t in chg_text for t in toks) or any(t in added for t in cited_texts):
            mapped.append(h)
    facts["mapped_hunks"] = len(mapped)
    if not mapped or all(_ws_only(h) for h in mapped):
        return done("noop", "no mapped hunk, or every mapped hunk is whitespace-only", **facts)

    wins = []
    for h in mapped:
        a, b = h["after_range"]
        wins.append([max(1, a), max(a, b)])
    wins.sort()
    merged = []
    for a, b in wins:
        if merged and a <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    after_passage = _join_windows(after_lines, merged)
    facts["after_passage"] = after_passage
    facts["diff"] = "\n".join(h["diff"] for h in mapped)

    deps, unresolved = find_dependencies(after_lines, after_passage, merged)
    facts["n_deps_needed"], facts["unresolved_refs"] = len(deps), unresolved
    if len(deps) > MAX_DEPS:
        return done("deps", f"{len(deps)} dependency passages needed (limit {MAX_DEPS})", **facts)
    facts["dependencies"] = {f"d{i}": d for i, d in enumerate(deps, 1)}
    pk = done("ok", "eligible", **facts)
    if oversize(packet_state(pk), len(deps)):
        pk.precheck, pk.reason = "oversize", "state over the request size limits (no truncation)"
        return pk
    pk.est_tokens = int(len(canonical_bytes(build_request(packet_state(pk), questions_for(len(deps))))) / C.RESERVE_BYTES_PER_TOKEN) + 1
    return pk
