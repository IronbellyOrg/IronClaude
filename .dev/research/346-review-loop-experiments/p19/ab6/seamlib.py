"""Shared plumbing for the ab6 Jev seams A1 (support), A2 (observability), A3 (novelty).  Python stdlib only.

* paths and the 13-spec list;
* spec parsing helpers on top of the PN2 lint parser (p16/ab4/reqlint.py);
* packet scrubbing (the privacy guard of the Jev adapter refuses owner names, home paths and github URLs);
* the Jev glue: a mock transport (deterministic, with failure modes), client construction with the J-budget ceilings,
  `ask_packet` (answer validation and fallback: any error or `insufficient` is NO hint), hint rendering helpers.

No function here reads or prints the Jev key.  Mock mode never sends anything and never uses the real key."""
import contextlib
import hashlib
import json
import math
import os
import pathlib
import re
import sys
import tomllib

SP = pathlib.Path(os.environ.get("SP", "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad"))
SEAMS = pathlib.Path(os.environ.get("AB6_ROOT", str(SP / "p19" / "ab6")))
JEV = SP / "p15" / "jev"
REQLINT_DIR = SP / "p16" / "ab4"
for _p in (JEV, REQLINT_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
sys.dont_write_bytecode = True

import reqlint  # noqa: E402  (PN2 lint parser)
from jevlib import config as C  # noqa: E402
from jevlib.budget import Budget, BudgetExhausted, usd  # noqa: E402
from jevlib.cache import ResponseCache  # noqa: E402
from jevlib.client import JevClient, KeyMissing, KeyRejected  # noqa: E402
from jevlib.journal import Journal  # noqa: E402
from jevlib.questions import build_request, canonical_bytes, choice  # noqa: E402
from jevlib.transport import MockStep, MockTransport, TransportTimeout, fake_answer  # noqa: E402

DECISION = SEAMS / "decision.toml"
EXPERIMENT = "AB6"
DATA_CLASSES = {"s1_spec", "stage2_artifact"}   # spec rows are S1 spec text; R2 reports / diffs are stage-2 artifacts


# ----------------------------------------------------------------------------- inputs
def decision(path=DECISION) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_specs13(path=None) -> list:
    path = path or os.environ.get("AB6_SPECS") or SEAMS / "specs-shadow.json"
    return json.loads(pathlib.Path(path).read_text())


def spec_text(entry) -> str:
    return pathlib.Path(entry["spec"]).read_text(encoding="utf-8")


def ledger_defects() -> list:
    return json.loads((SP / "p17" / "ledger.json").read_text())["defects"]


def ledger_status(entry) -> dict:
    """{defect id: status} for a spec entry.  The original spec has no scorer output: every ledger defect is PRESENT by definition."""
    if entry.get("ledger_status"):
        d = json.loads(pathlib.Path(entry["ledger_status"]).read_text())
        return {x["id"]: x["status"] for x in d["defects"]}
    return {x["id"]: "PRESENT" for x in ledger_defects()}


RESOLVED = ("FIXED", "DELETED_OK")


def is_residual(status: str) -> bool:
    return status not in RESOLVED


def line_map(orig: str, new: str):
    """Map original line numbers to the lines of `new` (difflib opcodes): {orig_line: [new lines]} ([] when deleted).
    A replaced block of m old and n new lines maps old line k to the proportional slice of the n new lines (at least one line)."""
    import difflib
    a, b = orig.split("\n"), new.split("\n")
    m = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        for i in range(i1, i2):
            if tag == "equal":
                m[i + 1] = [j1 + (i - i1) + 1]
            elif tag == "replace":
                mm, nn, k = i2 - i1, j2 - j1, i - i1
                lo = (k * nn) // mm
                hi = max(((k + 1) * nn) // mm, lo + 1)
                m[i + 1] = [j1 + x + 1 for x in range(lo, min(hi, nn))]
            else:
                m[i + 1] = []
    return m


# ----------------------------------------------------------------------------- text helpers
_SCRUBS = [
    (re.compile(r"https?://github\.com/\S+"), "<repo-url>"),
    (re.compile(r"IronbellyOrg/IronClaude"), "<fork-repo>"),
    (re.compile(r"IronbellyOrg"), "<fork-owner>"),
    (re.compile(r"SuperClaude-Org\S*"), "<upstream-repo>"),
    (re.compile(r"github\.com/"), "<host>/"),
    (re.compile(r"/home/[^\s`'\"]*"), "<abs-path>"),
    (re.compile(r"/root/[^\s`'\"]*"), "<abs-path>"),
    (re.compile(r"/tmp/claude[^\s`'\"]*"), "<abs-path>"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"), "<email>"),
    (re.compile(r"JEV_API_KEY"), "<key-env>"),
]


def scrub(text: str) -> str:
    """Remove strings the Jev privacy guard refuses (owner names, absolute paths, repo URLs).  Deterministic; applied to every packet."""
    for rx, rep in _SCRUBS:
        text = rx.sub(rep, text)
    return text


def scrub_obj(o):
    """scrub() applied to every string of a JSON-like object (keys are left alone)."""
    if isinstance(o, str):
        return scrub(o)
    if isinstance(o, list):
        return [scrub_obj(x) for x in o]
    if isinstance(o, dict):
        return {k: scrub_obj(v) for k, v in o.items()}
    return o


def clip(text: str, n: int) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def sha(obj) -> str:
    b = obj if isinstance(obj, bytes) else json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(b).hexdigest()


def plain(cell: str) -> str:
    """Cell text without bold markers; code ticks stay (they delimit commands for the reader)."""
    return (cell or "").replace("**", "")


def strip_md(cell: str) -> str:
    """Cell text without markdown emphasis and code ticks (ids and words stay)."""
    return re.sub(r"[`*]", "", cell or "")


# ----------------------------------------------------------------------------- spec parsing
def parse_spec(text: str):
    return reqlint.parse(text)


def find_tables(doc, *words):
    """Tables whose header contains every word (case-insensitive substring of some header cell)."""
    out = []
    for t in doc.tables:
        heads = [h.lower() for h in t.header]
        if all(any(w in h for h in heads) for w in words):
            out.append(t)
    return out


def heading_line(doc, pattern: str):
    rx = re.compile(pattern, re.I)
    for h in doc.headings:
        if rx.search(h.title):
            return h
    return None


def section_range(doc, h) -> tuple:
    """(first_line, last_line) of the section opened by heading h (up to the next heading of the same or higher level)."""
    end = len(doc.lines)
    for g in doc.headings:
        if g.line > h.line and g.level <= h.level:
            end = g.line - 1
            break
    return h.line, end


PHASE_RE = re.compile(r"\bP([0-4])\b")
ID_TOKEN_RE = re.compile(r"\b(?:WC|SA|AC|AC-C|AC-[0-4])\b")
CMD_NAMES = ["adversarial", "brainstorm", "cleanup-audit", "index-repo", "init-lite", "reflect", "release-split", "tdd", "troubleshoot",
             "workflow", "analyze", "auggie-review", "build", "business-panel", "cleanup", "cli-eval", "cli-portify", "design", "document",
             "explain", "implement", "improve", "index", "load", "post-release", "pr-submit", "recommend", "research", "review-translation",
             "roadmap", "save", "spec-panel", "task", "tasklist", "test", "validate-roadmap", "validate-tests"]
# bare words that are also ordinary English: a command only when written /sc:name or `name`
COMMON_CMD_WORDS = {"build", "cleanup", "design", "document", "explain", "implement", "improve", "index", "load", "recommend", "research",
                    "roadmap", "save", "task", "test", "analyze", "reflect", "workflow"}


def commands_in(text: str) -> list:
    """Command names mentioned in text: `/sc:name`, `name` in backticks, or a distinctive bare name."""
    found = set()
    t = text
    for n in CMD_NAMES:
        esc = re.escape(n)
        if re.search(rf"/sc:{esc}(?![\w-])", t) or re.search(rf"`{esc}`", t):
            found.add(n)
        elif n not in COMMON_CMD_WORDS and re.search(rf"(?<![\w/-]){esc}(?![\w-])", t):
            found.add(n)
    # longer names win over their prefixes ("cleanup" vs "cleanup-audit", "index" vs "index-repo", "task" vs "tasklist")
    for n in list(found):
        if any(o != n and o.startswith(n + "-") and o in found for o in found) or (n == "task" and "tasklist" in found and not re.search(r"`task`|/sc:task(?![\w-])", t)):
            found.discard(n)
    return sorted(found)


# ----------------------------------------------------------------------------- Jev glue
MOCK_KEY = "MOCK-TRANSPORT-NOT-A-KEY"


def _choice_body(req: dict, pick: dict, prob: float = 0.8) -> dict:
    """A syntactically valid response where question name -> chosen option (pick), probability `prob` on it."""
    answers = {}
    for name, q in sorted(req["questions"].items()):
        opts = list(q["criteria"])
        c = pick.get(name, opts[-1])
        rest = [o for o in opts if o != c]
        probs = {c: prob}
        for o in rest:
            probs[o] = (1.0 - prob) / len(rest)
        answers[name] = {"type": "choice", "choice": c, "confidence": prob, "probabilities": probs}
    return {"model": C.MODEL, "answers": answers,
            "usage": {"input_tokens": max(1, len(canonical_bytes(req)) // 4), "output_tokens": 6}}


def mock_script(mode: str = "ok", seed: int = 0, chooser=None):
    """A deterministic fake transport script (callable(req)->MockStep).

    modes: ok (valid, option derived from the request hash), insufficient, malformed, timeout, http500, wrongmodel, mixed
    (cycle over ok / insufficient / malformed / timeout by request hash), chooser (callable(req)->{name: option}, valid)."""
    def one(req, m):
        h = int(hashlib.sha256(canonical_bytes(req) + str(seed).encode()).hexdigest()[:8], 16)
        if m == "ok":
            if chooser is not None:
                return MockStep(200, _choice_body(req, chooser(req)))
            return MockStep(200, fake_answer(req, rng_seed=h))
        if m == "insufficient":
            return MockStep(200, _choice_body(req, {n: "insufficient" for n in req["questions"]}))
        if m == "malformed":
            return MockStep(200, b"{not json")
        if m == "timeout":
            return MockStep(exc=TransportTimeout("mock timeout"))
        if m == "http500":
            return MockStep(500, b"server error")
        if m == "wrongmodel":
            body = fake_answer(req, rng_seed=h)
            body["model"] = "jev-0.0.0"
            return MockStep(200, body)
        raise ValueError(mode)

    def script(req):
        if mode == "mixed":
            h = int(hashlib.sha256(canonical_bytes(req) + str(seed).encode()).hexdigest()[:8], 16)
            return one(req, ["ok", "ok", "insufficient", "malformed", "timeout", "ok"][h % 6])
        return one(req, mode)
    return script


@contextlib.contextmanager
def mock_env():
    """Mock mode needs a non-empty key variable for the client's key step; it is a placeholder, and the real value (if any) is restored."""
    old = os.environ.get(C.KEY_ENV)
    os.environ[C.KEY_ENV] = MOCK_KEY
    try:
        yield
    finally:
        if old is None:
            os.environ.pop(C.KEY_ENV, None)
        else:
            os.environ[C.KEY_ENV] = old


class Runner:
    """One Jev run context: client + budget + journal.  `ask` returns an Outcome and never raises on a Jev failure
    (KeyMissing / KeyRejected propagate: a configuration error is never a fallback)."""

    def __init__(self, *, seam: str, mode: str, out_dir: pathlib.Path, mock_mode: str = "ok", mock_seed: int = 0, chooser=None,
                 dec=None, ceiling_usd=None, ceiling_tokens=None, live_ledger=None, sleep=None, use_cache=True):
        import time as _t
        sleep = sleep if sleep is not None else (_t.sleep if mode == "live" else (lambda s: None))   # the J1.5 backoff is real only on a live run
        self.seam, self.mode = seam, mode
        self.dec = dec or decision()
        self.out_dir = pathlib.Path(out_dir)
        self.phase = f"replay-{seam}"
        cu = self.dec["jev"]["offline_ceiling_usd"] if ceiling_usd is None else ceiling_usd
        ct = self.dec["jev"]["offline_ceiling_input_tokens"] if ceiling_tokens is None else ceiling_tokens
        self.out_dir.mkdir(parents=True, exist_ok=True)
        if mode == "live":
            ledger = pathlib.Path(live_ledger or SEAMS / "budget" / "ab6.json")
            jpath = SEAMS / "journal" / f"jev-{seam}.jsonl"
            cache = ResponseCache(SEAMS / "cache") if use_cache else None
            transport = None
        else:
            ledger = self.out_dir / "mock-budget.json"
            for p in (ledger, pathlib.Path(str(ledger) + ".lock")):
                if p.exists():
                    p.unlink()
            jpath = self.out_dir / "mock-journal.jsonl"
            if jpath.exists():
                jpath.unlink()
            cache = None
            transport = MockTransport(mock_script(mock_mode, mock_seed, chooser))
        self.transport = transport
        self.budget = Budget(ledger, ceiling_usd=cu, ceiling_input_tokens=ct)
        self.journal = Journal(jpath)
        self.client = JevClient(experiment=EXPERIMENT, phase=self.phase, budget=self.budget, journal=self.journal, transport=transport,
                                live=True, cache=cache, sleep=sleep)
        # dry client for the pre-flight manifest: never touches the real ledger, never makes a network object
        self._dry_ledger = self.out_dir / "dryrun-budget.json"
        for p in (self._dry_ledger, pathlib.Path(str(self._dry_ledger) + ".lock")):
            if p.exists():
                p.unlink()
        self.dry = JevClient(experiment=EXPERIMENT, phase="dryrun", budget=Budget(self._dry_ledger, ceiling_usd=1e6, ceiling_input_tokens=10 ** 12),
                             journal=Journal(self.out_dir / "dryrun-journal.jsonl"), live=False)
        self.stats = {"calls": 0, "ok": 0, "fallback": 0, "input_tokens": 0, "est_tokens": 0, "status": {}, "usd": 0.0}

    # ---- pre-flight (J4): every request built with live=False, reservation = estimate x 1.2, before the first paid call
    def preflight(self, items) -> dict:
        n = est = priv = over = 0
        for it in items:
            r = self.dry.ask(it["state"], it["questions"], case_id=it["id"], qset_version=it["qset"], data_classes=set(it.get("data_classes") or DATA_CLASSES),
                             purpose=f"{self.seam} preflight")
            n += 1
            body = canonical_bytes(build_request(it["state"], it["questions"]))
            est += int(math.ceil(len(body) / C.RESERVE_BYTES_PER_TOKEN))
            if r.status == "refused" and r.error == "privacy":
                priv += 1
            elif r.status == "refused" and r.error == "oversize":
                over += 1
            elif not (r.status == "refused" and r.error == "dry_run"):
                raise RuntimeError(f"unexpected dry-run result {r.status}/{r.error} for {it['id']}")
        reserve = int(est * 1.2) + 1
        return {"requests": n, "est_tokens": est, "reserve_tokens": reserve, "reserve_usd": usd(reserve), "privacy_refused": priv, "oversize_refused": over}

    def reserve(self, tokens: int):
        self.budget.reserve_phase(self.phase, tokens)      # raises BudgetExhausted: the caller writes BLOCKED-BUDGET and makes no call

    def release(self):
        self.budget.release_phase(self.phase)

    def ask(self, item, *, purpose=None) -> dict:
        r = self.client.ask(item["state"], item["questions"], case_id=item["id"], qset_version=item["qset"],
                            data_classes=set(item.get("data_classes") or DATA_CLASSES), purpose=purpose or f"{self.seam} replay")
        out = outcome(r, item)
        self.stats["calls"] += 1
        self.stats["status"][out["status"] if out["status"] == "ok" else f"{r.status}/{r.error}"] = self.stats["status"].get(
            out["status"] if out["status"] == "ok" else f"{r.status}/{r.error}", 0) + 1
        if out["status"] == "ok":
            self.stats["ok"] += 1
        else:
            self.stats["fallback"] += 1
        if r.usage:
            self.stats["input_tokens"] += r.usage["input_tokens"]
        return out

    def finish(self) -> dict:
        st = self.budget.state()
        self.stats["usd"] = st["spent_usd"]
        self.stats["spent_tokens"] = st["spent_tokens"]
        return self.stats


def outcome(r, item) -> dict:
    """Validate a client Result against the item's question and reduce it to an Outcome.

    status 'ok' only when Jev returned a valid answer; `usable` is True only for an ok answer that is not `insufficient`.
    Everything else (invalid, unavailable, refused, insufficient) is a fallback: NO hint."""
    qname = next(iter(item["questions"]))
    allowed = set(item["questions"][qname]["criteria"])
    base = {"id": item["id"], "question": qname, "status": r.status, "error": r.error, "choice": None, "probs": None, "confidence": None,
            "usable": False, "fallback": None, "tokens": (r.usage or {}).get("input_tokens"), "attempts": r.attempts, "request_sha256": r.request_sha256}
    if r.status != "ok":
        base["fallback"] = f"{r.status}:{r.error}"
        return base
    a = (r.answers or {}).get(qname)
    if not a or a.get("type") != "choice" or a.get("choice") not in allowed:
        base["status"], base["error"], base["fallback"] = "invalid", "answer_shape", "invalid:answer_shape"
        return base
    base.update({"choice": a["choice"], "probs": a["probs"], "confidence": a["confidence"]})
    if a["choice"] == "insufficient":
        base["fallback"] = "insufficient"
        return base
    base["usable"] = True
    return base


def question_item(item_id, qset, state, qname, qdef, data_classes=None, **extra) -> dict:
    d = {"id": item_id, "qset": qset, "state": scrub_obj(state), "questions": {qname: qdef}, "data_classes": sorted(data_classes or DATA_CLASSES)}
    d.update(extra)
    return d


def packet_bytes(item) -> int:
    return len(canonical_bytes(build_request(item["state"], item["questions"])))


def write_json(path, obj):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")
