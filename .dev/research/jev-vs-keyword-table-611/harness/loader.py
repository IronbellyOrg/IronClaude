"""Loader: where every file lives, how it is hashed, and how the rule file, the corpus and the table answers are read.

One job: read the frozen files.  It owns hashing (``sha256_file``), so no other module computes a file hash itself.
"""
import hashlib
import json
import pathlib
import re

EXPERIMENT = pathlib.Path(__file__).resolve().parents[1]
JEVLIB_DIR = EXPERIMENT.parent / "346-review-loop-experiments" / "p15" / "jev" / "jevlib"

TYPES = ("bug", "build", "performance", "deployment", "security", "test")
LABELS = TYPES + ("ambiguous", "none-fit")
CODE_FILES = ("questions.py", "harness/loader.py", "harness/spend.py", "harness/gate.py", "harness/events.py",
              "harness/scorer.py", "harness/runner.py")

RULE_KEYS = ("status", "agreed_by", "agreed_at", "relayed_owner_words", "alpha_inverse", "median_limit_s", "slowest_limit_s",
             "attempt_timeout_s", "median_population", "rerun_policy", "p90_method", "spend_cap_usd", "noul_low", "noul_high",
             "noul_low_operator", "noul_high_operator", "unresolved_failure_invalid_count")
_INTS = ("alpha_inverse", "unresolved_failure_invalid_count")
_FLOATS = ("median_limit_s", "slowest_limit_s", "attempt_timeout_s", "spend_cap_usd", "noul_low", "noul_high")
CORPUS_FIELDS = ("id", "text", "source", "retrieved_on", "selection_reason", "label", "label_basis", "labeller", "labelled_on",
                 "seen_by_table")
PROVENANCE_FIELDS = ("retrieved_on", "selection_reason", "label_basis", "labeller", "labelled_on")   # must be non-empty text
UNSET = "UNSET"
# the one live route: the company gateway's native TypeSafe route (no /cli prefix, which answers 404); the runner sends here and the
# lead's go must name it (``events.py go`` records it, Gate 2 checks it), so a go given for another route never opens this one
GATEWAY_URL = "http://192.168.133.101:4000/typesafe/v1/systemone"
_PLAIN_NAME = re.compile(r"[A-Za-z0-9_.-]+")


def is_plain_name(value):
    """True for a run id or a rescore name that is safe as one path component: letters, digits, dot, underscore and hyphen,
    and not ``.`` or ``..``."""
    return isinstance(value, str) and bool(_PLAIN_NAME.fullmatch(value)) and value not in (".", "..")


TABLE_METHODS = ("person reading the prose", "skill execution")


class LoadError(ValueError):
    """A frozen file is missing, malformed or breaks a rule; the message names the cause, never the matched text."""


def require_own_root(paths):
    """The code and the questions that run are imported from the experiment folder this module was loaded from, so a run or a
    decisional score on any other ``--root`` would hash one set of files and execute another."""
    if pathlib.Path(paths.root).resolve() != EXPERIMENT.resolve():
        raise LoadError("--root is not the experiment folder this code was loaded from: the files it hashes would not be the code "
                        "that runs")


class Paths:
    """Every file location of the experiment, from one root (the experiment folder by default)."""

    def __init__(self, root=None, jevlib_dir=None):
        self.root = pathlib.Path(root) if root is not None else EXPERIMENT
        self.jevlib_dir = pathlib.Path(jevlib_dir) if jevlib_dir is not None else JEVLIB_DIR
        r = self.root
        self.corpus = r / "corpus" / "corpus.jsonl"
        self.selection_criteria = r / "corpus" / "selection-criteria.md"
        self.labelling_record = r / "corpus" / "labelling-record.md"
        self.questions_py = r / "questions.py"
        self.rule = r / "decision-rule.md"
        self.table_answers = r / "table" / "table-answers.jsonl"
        self.table_provenance = r / "table" / "table-provenance.md"
        self.manifest = r / "manifest.json"
        self.events = r / "events.jsonl"
        self.ledger = r / "ledger" / "spend.json"
        self.runs = r / "runs"
        self.report = r / "report.md"
        self.decision_record = r / "decision-record.md"
        self.rescores = r / "rescores"
        self.tests_dir = r / "harness" / "tests"

    def code_files(self):
        """The experiment's own code files, as paths under the root."""
        return [self.root / c for c in CODE_FILES]

    def jevlib_files(self):
        """The ``.py`` files directly inside the jevlib folder, sorted by name; never a folder walk, so no cache folder."""
        return sorted(p for p in self.jevlib_dir.glob("*.py") if p.is_file())


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _section(text, heading):
    """The text under ``## <heading>`` up to the next ``## `` heading, or ''."""
    out, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if on:
                break
            on = line[3:].strip() == heading
            continue
        if on:
            out.append(line)
    return "\n".join(out).strip()


def load_rule(path, for_scoring=False):
    """Read the rule file.  Refuses a missing key, a status other than AGREED, an empty who, when or agreement text, and, with
    ``for_scoring``, any value still ``UNSET``.  Without ``for_scoring`` an unset value loads as the string ``UNSET``."""
    path = pathlib.Path(path)
    if not path.is_file():
        raise LoadError(f"rule file missing: {path.name}")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise LoadError("rule file has no front matter")
    rule, end = {}, None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end = i
            break
        if ": " in line:
            k, v = line.split(": ", 1)
            rule[k.strip()] = v.strip()
        elif line.strip().endswith(":"):
            rule[line.strip()[:-1]] = ""
    if end is None:
        raise LoadError("rule file front matter is not closed")
    for k in RULE_KEYS:
        if k not in rule:
            raise LoadError(f"rule file lacks the key {k}")
    if rule["status"] != "AGREED":
        raise LoadError(f"rule status is {rule['status']!r}, not AGREED")
    for k in ("agreed_by", "agreed_at", "relayed_owner_words"):
        if not rule[k]:
            raise LoadError(f"rule key {k} is empty")
    agreement = _section("\n".join(lines[end + 1:]), "Agreement text (verbatim)")
    if not agreement:
        raise LoadError("rule file has no verbatim agreement text")
    rule["agreement_text"] = agreement
    for k in _INTS:
        if rule[k] != UNSET:
            rule[k] = _number(k, rule[k], int)
    for k in _FLOATS:
        if rule[k] != UNSET:
            rule[k] = _number(k, rule[k], float)
    if rule["noul_low_operator"] not in (UNSET, "lt", "le"):
        raise LoadError("noul_low_operator must be lt or le")
    if rule["noul_high_operator"] not in (UNSET, "gt", "ge"):
        raise LoadError("noul_high_operator must be gt or ge")
    if for_scoring:
        unset = [k for k in RULE_KEYS if rule[k] == UNSET]
        if unset:
            raise LoadError("rule values still UNSET: " + ", ".join(unset))
    return rule


def _number(key, raw, kind):
    try:
        return kind(raw)
    except ValueError:
        raise LoadError(f"rule key {key} is not a number: {raw!r}") from None


def _jsonl(path, what):
    path = pathlib.Path(path)
    if not path.is_file():
        raise LoadError(f"{what} missing: {path.name}")
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            raise LoadError(f"{what} line {n} is not JSON") from None
        if not isinstance(row, dict):
            raise LoadError(f"{what} line {n} is not an object")
        rows.append(row)
    return rows


def load_corpus(path):
    """Read and check the frozen corpus.  Every prompt is screened with jevlib's privacy check as public data; a refusal is
    reported with the prompt id and the reason, never the matched text."""
    from jevlib.manifest import privacy_violation
    rows = _jsonl(path, "corpus")
    seen_ids, seen_text = set(), {}
    for r in rows:
        missing = [f for f in CORPUS_FIELDS if f not in r]
        if missing:
            raise LoadError(f"corpus row {r.get('id', '?')} lacks {', '.join(missing)}")
        rid = r["id"]
        if not isinstance(rid, str) or not rid:
            raise LoadError("corpus row has no id")
        if rid in seen_ids:
            raise LoadError(f"duplicate corpus id {rid}")
        seen_ids.add(rid)
        if not isinstance(r["text"], str) or not r["text"].strip():
            raise LoadError(f"corpus row {rid} has no text")
        if r["text"] in seen_text:
            raise LoadError(f"corpus rows {seen_text[r['text']]} and {rid} hold the same text")
        seen_text[r["text"]] = rid
        if not isinstance(r["source"], str) or not r["source"].strip():
            raise LoadError(f"corpus row {rid} has no public source")
        if r["label"] not in LABELS:
            raise LoadError(f"corpus row {rid} has a label outside the allowed set")
        for field in PROVENANCE_FIELDS:
            if not isinstance(r[field], str) or not r[field].strip():
                raise LoadError(f"corpus row {rid} has an empty {field}")
        if not isinstance(r["seen_by_table"], bool):
            raise LoadError(f"corpus row {rid} has a seen_by_table that is not true or false")
        why = privacy_violation({"prompt": r["text"]}, ["public"])
        if why:
            raise LoadError(f"corpus row {rid} refused by the privacy screen: {why}")
    labels = {r["label"] for r in rows}
    for t in TYPES:
        if t not in labels:
            raise LoadError(f"corpus has no row labelled {t}")
    for extra in ("ambiguous", "none-fit"):
        if extra not in labels:
            raise LoadError(f"corpus has no row labelled {extra}")
    return rows


def load_table_answers(path, corpus_ids=None):
    """The table answers, one JSON object per line (prompt_id, answer or null, cues, rows, method).

    With ``corpus_ids`` the file is also checked against the corpus: exactly one row for every id, an explicit ``answer`` that is
    null or one of the six types, the ``cues``, ``rows`` and ``method`` the table procedure records, no duplicate and no unknown id.
    A refusal names the prompt id, never prompt text."""
    rows = _jsonl(path, "table answers")
    for r in rows:
        if "prompt_id" not in r:
            raise LoadError("table answer row lacks prompt_id")
    if corpus_ids is None:
        return rows
    seen = set()
    for r in rows:
        pid = r["prompt_id"]
        if pid in seen:
            raise LoadError(f"table answers hold prompt {pid} more than once")
        seen.add(pid)
        if "answer" not in r:
            raise LoadError(f"table answer row {pid} has no answer field (an unset answer is an explicit null)")
        if r["answer"] is not None and r["answer"] not in TYPES:
            raise LoadError(f"table answer row {pid} has an answer that is neither null nor one of the six types")
        # the evidence the table procedure records for every answer
        if not isinstance(r.get("cues"), list) or not all(isinstance(c, str) for c in r["cues"]):
            raise LoadError(f"table answer row {pid} needs cues: a list of the cue phrases found (empty when none)")
        if not isinstance(r.get("rows"), list) or not all(isinstance(x, str) and x in TYPES for x in r["rows"]):
            raise LoadError(f"table answer row {pid} needs rows: a list of the matched row names (empty when none), each one of the six types")
        if r.get("method") not in TABLE_METHODS:
            raise LoadError(f"table answer row {pid} needs a method: one of {', '.join(TABLE_METHODS)}")
    wanted = set(corpus_ids)
    if seen - wanted:
        raise LoadError("table answers name a prompt id that is not in the corpus: " + ", ".join(sorted(map(str, seen - wanted))))
    if wanted - seen:
        raise LoadError("table answers lack a row for corpus prompt: " + ", ".join(sorted(wanted - seen)))
    return rows
