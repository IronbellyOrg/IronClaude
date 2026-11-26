efc4c83de87a93ecad3bdab9b50b397be6937550
Review one task for spec compliance.

Task brief: ## Task 2: Write the rule file and the loader

Depends on: Task 1

Create `.dev/research/jev-vs-keyword-table-611/decision-rule.md`, `.dev/research/jev-vs-keyword-table-611/harness/loader.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py`.

`decision-rule.md` starts with a front-matter block of plain `key: value` lines (stdlib parser, no nesting) holding: `status: AGREED`, `agreed_by`, `agreed_at: 2026-11-26`, `relayed_owner_words`, `alpha_inverse: 20`, `median_limit_s: 2`, `slowest_limit_s: 5`, `attempt_timeout_s: 10`, `median_population: answered_only`, `rerun_policy: one_per_prompt`, `p90_method: nearest_rank`, `spend_cap_usd: 1.0`, `noul_low: 0.3`, `noul_high: 0.7`, `noul_low_operator: UNSET`, `noul_high_operator: UNSET` and `unresolved_failure_invalid_count: UNSET`. The valid operators are `lt` or `le` for the low edge and `gt` or `ge` for the high edge. Its body holds a section `## Agreement text (verbatim)` with the IronFlow reply of 2026-11-26 word for word as in the Constraints above, and a section `## Rule in words` restating the agreed rule from the Constraints.

`loader.py` provides:
- `Paths(root=None)`: every file location of the experiment from one root, which defaults to the experiment folder found from the module's own location. It gives `corpus`, `selection_criteria`, `labelling_record`, `questions_py`, `rule`, `table_answers`, `table_provenance`, `manifest`, `events`, `ledger`, `runs`, `report`, `decision_record` and `rescores`, plus `jevlib_dir` (the existing `jevlib` folder by default, overridable for tests), `code_files()` (`questions.py` and the `harness` modules `loader`, `spend`, `gate`, `events`, `scorer` and `runner`) and `jevlib_files()` (the `.py` files directly inside `jevlib_dir`, sorted by name, never a folder walk, so `__pycache__` is never hashed).
- `sha256_file(path)`, the only SHA-256 helper in the experiment.
- `load_rule(path, for_scoring=False)`: refuses when a required key is missing, when `status` is not `AGREED`, when `agreed_by`, `agreed_at` or the verbatim agreement text is empty, and, when `for_scoring` is true, when any value is `UNSET`. Without `for_scoring` an `UNSET` value loads as the string `UNSET`.
- `load_corpus(path)` and `load_table_answers(path)` (JSON lines). A corpus row has `id`, `text`, `source`, `retrieved_on`, `selection_reason`, `label` (one of the six types, `ambiguous` or `none-fit`), `label_basis`, `labeller`, `labelled_on` and `seen_by_table`. `load_corpus` rejects a missing public `source`, a duplicate `id`, the same `text` under two ids, a label outside the allowed set, a missing type among the six, no `ambiguous` row and no `none-fit` row, and runs `jevlib.manifest.privacy_violation` on each prompt with data class `public`, failing with the reason string and the prompt id (never the matched text).

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py -v` passes (requirement T-04 and the rule-file refusals of T-01).
- Tests show `load_rule` refuses `PROPOSED`, `PENDING`, an empty agreement text and a missing key, loads the file as committed with `UNSET` for exactly the three open fields, and refuses with `for_scoring=True` while an `UNSET` value remains.
- Tests show `load_corpus` rejects each case listed above, including a prompt containing a GitHub URL and one containing a home-directory path (the cases `jevlib.manifest.privacy_violation` refuses).
- Tests show `Paths` built on a temporary root gives only paths under that root (except `jevlib_dir`), and `jevlib_files()` lists only top-level `.py` names and omits a `__pycache__` folder.
- `decision-rule.md` as committed contains the verbatim IronFlow agreement text and the relayed owner words marked as relayed.

Acceptance criterion ids (in source order):
T2.AC1: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py -v` passes (requirement T-04 and the rule-file refusals of T-01).
T2.AC2: Tests show `load_rule` refuses `PROPOSED`, `PENDING`, an empty agreement text and a missing key, loads the file as committed with `UNSET` for exactly the three open fields, and refuses with `for_scoring=True` while an `UNSET` value remains.
T2.AC3: Tests show `load_corpus` rejects each case listed above, including a prompt containing a GitHub URL and one containing a home-directory path (the cases `jevlib.manifest.privacy_violation` refuses).
T2.AC4: Tests show `Paths` built on a temporary root gives only paths under that root (except `jevlib_dir`), and `jevlib_files()` lists only top-level `.py` names and omits a `__pycache__` folder.
T2.AC5: `decision-rule.md` as committed contains the verbatim IronFlow agreement text and the relayed owner words marked as relayed.
Global constraints: ## Constraints

- Scope is build and test only. No task sends a prompt to TypeSafe, reads `TYPESAFE_API_KEY` or `JEV_API_KEY` from the real environment, or opens a network connection. Tests use `MockTransport` and a socket guard, set a fake key with `monkeypatch.setenv`, and use a temporary experiment root for every file the gates, events, runner and scorer write. The live run is a coordinator action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md` (lines 145 to 165).
- Left for a person or the coordinator, not in this plan: choosing and labelling about 30 public prompts (a named human labeller is required), applying the keyword table to them (a session or person who sees prompts only, after Gate 1), the live run with `keyscan.py`, scoring and the report, and the updates on issues 611, 609 and 612. Tasks 7 and 8 produce the procedures, templates and instructions those steps need. The pull request that delivers this plan says `Refs #611` and lists parts B to E of section 8 of the design as left (Task 8 puts that sentence in the README).
- Nothing under `src/`, `tests/`, `.claude/` or the existing `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` folder is changed. `jevlib` is imported read-only, and only from its submodules (`client`, `budget`, `journal`, `transport`, `questions`, `manifest`, `config`), because `jevlib/__init__.py` exports only `MODEL`, `API_URL` and `KEY_ENV`.
- Spend cap is 1 dollar in total; public prompts only; the key is never printed, logged, written to a file, put on a command line or put in a pull request. The runner copies `TYPESAFE_API_KEY` into `JEV_API_KEY` inside its own process only, because `jevlib.config.KEY_ENV` is `JEV_API_KEY`.
- Agreed decision rule (AGREED 2026-11-26 by the IronFlow session and the build agent, relayed by the lead; Clay's own words as quoted by the IronFlow session, not typed by Clay: "you and the agent debate whats correct way to handle this and do it").
- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. Per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
- Still open, so written as `UNSET` in the rule file: the operators at exactly 0.3 and 0.7 for the Noul band, and the count of unresolved failures that makes a run invalid. Gate 1 accepts `UNSET` and does not freeze the rule file's hash. The scorer, the `freeze-rule` command and Gate 2 refuse any `UNSET` value, and `freeze-rule` is the step that freezes the rule file's hash after the owner has filled the fields.
- The real client behaves differently from a mock-backed dry run: `JevClient` with `live=False` builds, screens and budgets the request, then returns `refused` with error `dry_run` before any transport call. So the runner has two subcommands: `run` needs `--live`, both gates and the key; `rehearse` never posts and needs no gate and no key. Tests that need the transport path use `live=True`, an injected `MockTransport` and a fake `JEV_API_KEY`.
- Test run command, recorded by `gate.py record-tests`: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`. The repository's `testpaths` is `tests`, so tests under `.dev/` are only collected when this path is given.
- Each of the four command-line modules (`gate.py`, `events.py`, `runner.py` and `scorer.py`) inserts the existing `jevlib` folder and the experiment folder into `sys.path` itself, as `.dev/research/346-review-loop-experiments/p15/jev/probe.py` does (read-only reference), because only `conftest.py` does so for tests (finding M-12).
Start sha: efc4c83de87a93ecad3bdab9b50b397be6937550
Diff against the start snapshot: diff --git a/.dev/research/jev-vs-keyword-table-611/decision-rule.md b/.dev/research/jev-vs-keyword-table-611/decision-rule.md
new file mode 100644
index 000000000..453616aef
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/decision-rule.md
@@ -0,0 +1,43 @@
+---
+status: AGREED
+agreed_by: the IronFlow session and the build agent
+agreed_at: 2026-11-26
+relayed_owner_words: you and the agent debate whats correct way to handle this and do it
+alpha_inverse: 20
+median_limit_s: 2
+slowest_limit_s: 5
+attempt_timeout_s: 10
+median_population: answered_only
+rerun_policy: one_per_prompt
+p90_method: nearest_rank
+spend_cap_usd: 1.0
+noul_low: 0.3
+noul_high: 0.7
+noul_low_operator: UNSET
+noul_high_operator: UNSET
+unresolved_failure_invalid_count: UNSET
+---
+
+# Decision rule: does Jev beat the keyword table (issue 611)
+
+This file holds every policy value of the experiment. The scorer, the gates and the runner read it and invent nothing. Three values are still `UNSET` on purpose: the two operators at the edges of the Noul band (0.3 and 0.7) and the count of unresolved failures that makes a run invalid. The owner sets them before the rule file is frozen with `gate.py freeze-rule`; the scorer and Gate 2 refuse to run while any value is `UNSET`.
+
+## Agreement text (verbatim)
+
+"Reply from the IronFlow session: I agree with all five of your amendments, so the rule as written under "Decision rule as it stands" is AGREED, 26 Nov 2026, by the IronFlow session and this agent. You are right that 8-2 fails (56/1024 = 0.0547); the formula, computed in integers, is the rule. Agreed too: an unset answer is right for both sides on an ambiguous or none-fit prompt; one rerun per failed prompt, logged and counted against the cap, and scored not right if it fails again; client-side timing with a 10 second per-call timeout counted at its timeout value; and the 90th percentile in the report. On provenance, Clay's own words to me today, word for word: "you and the agent debate whats correct way to handle this and do it". Record that quote with the rule, mark the block AGREED, and go ahead within the 1 dollar cap and public prompts only."
+
+## Relayed owner words
+
+"you and the agent debate whats correct way to handle this and do it"
+
+These are Clay's own words as quoted by the IronFlow session. They were relayed: Clay did not type them into the build session. The agreement was made between the IronFlow session and the build agent, and the lead pasted it into the build session on 2026-11-26.
+
+## Rule in words
+
+- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
+- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
+- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. The per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
+- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
+- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
+- Spend: 1 dollar in total, public prompts only.
+- Still open (`UNSET` above): the operators at exactly 0.3 and 0.7 for the Noul band (`lt` or `le` for the low edge, `gt` or `ge` for the high edge), and the count of unresolved failures that makes a run invalid.
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/loader.py b/.dev/research/jev-vs-keyword-table-611/harness/loader.py
new file mode 100644
index 000000000..bcd4e3306
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/loader.py
@@ -0,0 +1,205 @@
+"""Loader: where every file lives, how it is hashed, and how the rule file, the corpus and the table answers are read.
+
+One job: read the frozen files.  It owns hashing (``sha256_file``), so no other module computes a file hash itself.
+"""
+import hashlib
+import json
+import pathlib
+
+EXPERIMENT = pathlib.Path(__file__).resolve().parents[1]
+JEVLIB_DIR = EXPERIMENT.parent / "346-review-loop-experiments" / "p15" / "jev" / "jevlib"
+
+TYPES = ("bug", "build", "performance", "deployment", "security", "test")
+LABELS = TYPES + ("ambiguous", "none-fit")
+CODE_FILES = ("questions.py", "harness/loader.py", "harness/spend.py", "harness/gate.py", "harness/events.py",
+              "harness/scorer.py", "harness/runner.py")
+
+RULE_KEYS = ("status", "agreed_by", "agreed_at", "relayed_owner_words", "alpha_inverse", "median_limit_s", "slowest_limit_s",
+             "attempt_timeout_s", "median_population", "rerun_policy", "p90_method", "spend_cap_usd", "noul_low", "noul_high",
+             "noul_low_operator", "noul_high_operator", "unresolved_failure_invalid_count")
+_INTS = ("alpha_inverse", "unresolved_failure_invalid_count")
+_FLOATS = ("median_limit_s", "slowest_limit_s", "attempt_timeout_s", "spend_cap_usd", "noul_low", "noul_high")
+CORPUS_FIELDS = ("id", "text", "source", "retrieved_on", "selection_reason", "label", "label_basis", "labeller", "labelled_on",
+                 "seen_by_table")
+UNSET = "UNSET"
+
+
+class LoadError(ValueError):
+    """A frozen file is missing, malformed or breaks a rule; the message names the cause, never the matched text."""
+
+
+class Paths:
+    """Every file location of the experiment, from one root (the experiment folder by default)."""
+
+    def __init__(self, root=None, jevlib_dir=None):
+        self.root = pathlib.Path(root) if root is not None else EXPERIMENT
+        self.jevlib_dir = pathlib.Path(jevlib_dir) if jevlib_dir is not None else JEVLIB_DIR
+        r = self.root
+        self.corpus = r / "corpus" / "corpus.jsonl"
+        self.selection_criteria = r / "corpus" / "selection-criteria.md"
+        self.labelling_record = r / "corpus" / "labelling-record.md"
+        self.questions_py = r / "questions.py"
+        self.rule = r / "decision-rule.md"
+        self.table_answers = r / "table" / "table-answers.jsonl"
+        self.table_provenance = r / "table" / "table-provenance.md"
+        self.manifest = r / "manifest.json"
+        self.events = r / "events.jsonl"
+        self.ledger = r / "ledger" / "spend.json"
+        self.runs = r / "runs"
+        self.report = r / "report.md"
+        self.decision_record = r / "decision-record.md"
+        self.rescores = r / "rescores"
+        self.tests_dir = r / "harness" / "tests"
+
+    def code_files(self):
+        """The experiment's own code files, as paths under the root."""
+        return [self.root / c for c in CODE_FILES]
+
+    def jevlib_files(self):
+        """The ``.py`` files directly inside the jevlib folder, sorted by name; never a folder walk, so no cache folder."""
+        return sorted(p for p in self.jevlib_dir.glob("*.py") if p.is_file())
+
+
+def sha256_file(path):
+    h = hashlib.sha256()
+    with open(path, "rb") as f:
+        for chunk in iter(lambda: f.read(65536), b""):
+            h.update(chunk)
+    return h.hexdigest()
+
+
+def _section(text, heading):
+    """The text under ``## <heading>`` up to the next ``## `` heading, or ''."""
+    out, on = [], False
+    for line in text.splitlines():
+        if line.startswith("## "):
+            if on:
+                break
+            on = line[3:].strip() == heading
+            continue
+        if on:
+            out.append(line)
+    return "\n".join(out).strip()
+
+
+def load_rule(path, for_scoring=False):
+    """Read the rule file.  Refuses a missing key, a status other than AGREED, an empty who, when or agreement text, and, with
+    ``for_scoring``, any value still ``UNSET``.  Without ``for_scoring`` an unset value loads as the string ``UNSET``."""
+    path = pathlib.Path(path)
+    if not path.is_file():
+        raise LoadError(f"rule file missing: {path.name}")
+    text = path.read_text(encoding="utf-8")
+    lines = text.splitlines()
+    if not lines or lines[0].strip() != "---":
+        raise LoadError("rule file has no front matter")
+    rule, end = {}, None
+    for i, line in enumerate(lines[1:], 1):
+        if line.strip() == "---":
+            end = i
+            break
+        if ": " in line:
+            k, v = line.split(": ", 1)
+            rule[k.strip()] = v.strip()
+        elif line.strip().endswith(":"):
+            rule[line.strip()[:-1]] = ""
+    if end is None:
+        raise LoadError("rule file front matter is not closed")
+    for k in RULE_KEYS:
+        if k not in rule:
+            raise LoadError(f"rule file lacks the key {k}")
+    if rule["status"] != "AGREED":
+        raise LoadError(f"rule status is {rule['status']!r}, not AGREED")
+    for k in ("agreed_by", "agreed_at", "relayed_owner_words"):
+        if not rule[k]:
+            raise LoadError(f"rule key {k} is empty")
+    agreement = _section("\n".join(lines[end + 1:]), "Agreement text (verbatim)")
+    if not agreement:
+        raise LoadError("rule file has no verbatim agreement text")
+    rule["agreement_text"] = agreement
+    for k in _INTS:
+        if rule[k] != UNSET:
+            rule[k] = _number(k, rule[k], int)
+    for k in _FLOATS:
+        if rule[k] != UNSET:
+            rule[k] = _number(k, rule[k], float)
+    if rule["noul_low_operator"] not in (UNSET, "lt", "le"):
+        raise LoadError("noul_low_operator must be lt or le")
+    if rule["noul_high_operator"] not in (UNSET, "gt", "ge"):
+        raise LoadError("noul_high_operator must be gt or ge")
+    if for_scoring:
+        unset = [k for k in RULE_KEYS if rule[k] == UNSET]
+        if unset:
+            raise LoadError("rule values still UNSET: " + ", ".join(unset))
+    return rule
+
+
+def _number(key, raw, kind):
+    try:
+        return kind(raw)
+    except ValueError:
+        raise LoadError(f"rule key {key} is not a number: {raw!r}") from None
+
+
+def _jsonl(path, what):
+    path = pathlib.Path(path)
+    if not path.is_file():
+        raise LoadError(f"{what} missing: {path.name}")
+    rows = []
+    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
+        if not line.strip():
+            continue
+        try:
+            row = json.loads(line)
+        except ValueError:
+            raise LoadError(f"{what} line {n} is not JSON") from None
+        if not isinstance(row, dict):
+            raise LoadError(f"{what} line {n} is not an object")
+        rows.append(row)
+    return rows
+
+
+def load_corpus(path):
+    """Read and check the frozen corpus.  Every prompt is screened with jevlib's privacy check as public data; a refusal is
+    reported with the prompt id and the reason, never the matched text."""
+    from jevlib.manifest import privacy_violation
+    rows = _jsonl(path, "corpus")
+    seen_ids, seen_text = set(), {}
+    for r in rows:
+        missing = [f for f in CORPUS_FIELDS if f not in r]
+        if missing:
+            raise LoadError(f"corpus row {r.get('id', '?')} lacks {', '.join(missing)}")
+        rid = r["id"]
+        if not isinstance(rid, str) or not rid:
+            raise LoadError("corpus row has no id")
+        if rid in seen_ids:
+            raise LoadError(f"duplicate corpus id {rid}")
+        seen_ids.add(rid)
+        if not isinstance(r["text"], str) or not r["text"].strip():
+            raise LoadError(f"corpus row {rid} has no text")
+        if r["text"] in seen_text:
+            raise LoadError(f"corpus rows {seen_text[r['text']]} and {rid} hold the same text")
+        seen_text[r["text"]] = rid
+        if not isinstance(r["source"], str) or not r["source"].strip():
+            raise LoadError(f"corpus row {rid} has no public source")
+        if r["label"] not in LABELS:
+            raise LoadError(f"corpus row {rid} has a label outside the allowed set")
+        why = privacy_violation({"prompt": r["text"]}, ["public"])
+        if why:
+            raise LoadError(f"corpus row {rid} refused by the privacy screen: {why}")
+    labels = {r["label"] for r in rows}
+    for t in TYPES:
+        if t not in labels:
+            raise LoadError(f"corpus has no row labelled {t}")
+    for extra in ("ambiguous", "none-fit"):
+        if extra not in labels:
+            raise LoadError(f"corpus has no row labelled {extra}")
+    return rows
+
+
+def load_table_answers(path):
+    """The table answers, one JSON object per line (prompt_id, answer or null, cues, rows, method)."""
+    rows = _jsonl(path, "table answers")
+    for r in rows:
+        if "prompt_id" not in r:
+            raise LoadError("table answer row lacks prompt_id")
+    return rows
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py
new file mode 100644
index 000000000..d4deb2fcf
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py
@@ -0,0 +1,177 @@
+import json
+import pathlib
+
+import pytest
+from harness import loader
+from harness.loader import LoadError, Paths
+
+RULE = loader.EXPERIMENT / "decision-rule.md"
+OPEN_FIELDS = {"noul_low_operator", "noul_high_operator", "unresolved_failure_invalid_count"}
+
+
+def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
+    s = RULE.read_text(encoding="utf-8") if text is None else text
+    if old is not None:
+        assert old in s
+        s = s.replace(old, new, 1)
+    if drop_line is not None:
+        s = "\n".join(line for line in s.splitlines() if not line.startswith(drop_line)) + "\n"
+    p = tmp_path / "decision-rule.md"
+    p.write_text(s, encoding="utf-8")
+    return p
+
+
+# ---- rule file (T-01 refusals, T-04)
+
+def test_committed_rule_loads_with_exactly_the_three_open_fields_unset():
+    rule = loader.load_rule(RULE)
+    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} == OPEN_FIELDS
+    assert rule["status"] == "AGREED" and rule["alpha_inverse"] == 20 and rule["attempt_timeout_s"] == 10.0
+    assert rule["median_limit_s"] == 2.0 and rule["slowest_limit_s"] == 5.0 and rule["spend_cap_usd"] == 1.0
+
+
+def test_committed_rule_holds_the_verbatim_agreement_and_marks_the_owner_words_relayed():
+    text = RULE.read_text(encoding="utf-8")
+    assert "I agree with all five of your amendments" in text and "56/1024 = 0.0547" in text
+    assert "you and the agent debate whats correct way to handle this and do it" in text
+    assert "relayed" in text.lower() and "did not type them" in text
+
+
+@pytest.mark.parametrize("status", ["PROPOSED", "PENDING"])
+def test_rule_refuses_a_status_other_than_agreed(tmp_path, status):
+    with pytest.raises(LoadError, match="not AGREED"):
+        loader.load_rule(_rule_copy(tmp_path, "status: AGREED", f"status: {status}"))
+
+
+def test_rule_refuses_an_empty_agreement_text(tmp_path):
+    s = RULE.read_text(encoding="utf-8")
+    head, _, rest = s.partition("## Agreement text (verbatim)")
+    _, _, tail = rest.partition("## Relayed owner words")
+    p = _rule_copy(tmp_path, text=head + "## Agreement text (verbatim)\n\n## Relayed owner words" + tail)
+    with pytest.raises(LoadError, match="agreement text"):
+        loader.load_rule(p)
+
+
+@pytest.mark.parametrize("key", ["agreed_by", "agreed_at", "relayed_owner_words"])
+def test_rule_refuses_an_empty_who_when_or_words(tmp_path, key):
+    lines = [(f"{key}:" if line.startswith(key + ":") else line) for line in RULE.read_text(encoding="utf-8").splitlines()]
+    p = _rule_copy(tmp_path, text="\n".join(lines) + "\n")
+    with pytest.raises(LoadError, match="empty"):
+        loader.load_rule(p)
+
+
+def test_rule_refuses_a_missing_key_and_a_missing_file(tmp_path):
+    with pytest.raises(LoadError, match="lacks the key alpha_inverse"):
+        loader.load_rule(_rule_copy(tmp_path, drop_line="alpha_inverse:"))
+    with pytest.raises(LoadError, match="missing"):
+        loader.load_rule(tmp_path / "nope.md")
+
+
+def test_rule_refuses_scoring_while_a_value_is_unset_and_accepts_it_when_all_are_set(tmp_path):
+    with pytest.raises(LoadError, match="UNSET"):
+        loader.load_rule(RULE, for_scoring=True)
+    s = RULE.read_text(encoding="utf-8")
+    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
+    s = s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3")
+    rule = loader.load_rule(_rule_copy(tmp_path, text=s), for_scoring=True)
+    assert rule["noul_low_operator"] == "le" and rule["unresolved_failure_invalid_count"] == 3
+
+
+def test_rule_refuses_an_operator_that_does_not_fit_its_edge(tmp_path):
+    with pytest.raises(LoadError, match="noul_low_operator"):
+        loader.load_rule(_rule_copy(tmp_path, "noul_low_operator: UNSET", "noul_low_operator: gt"))
+    with pytest.raises(LoadError, match="noul_high_operator"):
+        loader.load_rule(_rule_copy(tmp_path, "noul_high_operator: UNSET", "noul_high_operator: lt"))
+
+
+# ---- corpus (T-04)
+
+def _row(i, text, label, **kw):
+    r = {"id": f"p{i}", "text": text, "source": "https://example.org/issue/" + str(i), "retrieved_on": "2026-11-26",
+         "selection_reason": "r", "label": label, "label_basis": "b", "labeller": "a person", "labelled_on": "2026-11-26",
+         "seen_by_table": False}
+    r.update(kw)
+    return r
+
+
+def _good_rows():
+    labels = list(loader.TYPES) + ["ambiguous", "none-fit"]
+    return [_row(i, f"problem text number {i}", lab) for i, lab in enumerate(labels)]
+
+
+def _write(tmp_path, rows):
+    p = tmp_path / "corpus.jsonl"
+    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
+    return p
+
+
+def test_a_valid_corpus_loads(tmp_path):
+    rows = loader.load_corpus(_write(tmp_path, _good_rows()))
+    assert len(rows) == 8 and rows[0]["id"] == "p0"
+
+
+def _bad(rows, i, **kw):
+    rows[i] = dict(rows[i], **kw)
+    return rows
+
+
+@pytest.mark.parametrize("mutate,match", [
+    (lambda r: _bad(r, 0, source=""), "no public source"),
+    (lambda r: _bad(r, 1, id="p0"), "duplicate corpus id"),
+    (lambda r: _bad(r, 1, text="problem text number 0"), "same text"),
+    (lambda r: _bad(r, 2, label="urgent"), "outside the allowed set"),
+    (lambda r: _bad(r, 3, label="bug"), "no row labelled deployment"),
+    (lambda r: _bad(r, 6, label="bug"), "no row labelled ambiguous"),
+    (lambda r: _bad(r, 7, label="bug"), "no row labelled none-fit"),
+])
+def test_corpus_rejects_each_rule_break(tmp_path, mutate, match):
+    with pytest.raises(LoadError, match=match):
+        loader.load_corpus(_write(tmp_path, mutate(_good_rows())))
+
+
+@pytest.mark.parametrize("text,reason", [
+    ("see https://github.com/example/project/issues/4 for details", "github_url"),
+    ("the file is at /home/someone/project/main.py", "path_home"),
+])
+def test_corpus_refuses_a_prompt_the_privacy_screen_refuses_without_echoing_it(tmp_path, text, reason):
+    rows = _bad(_good_rows(), 0, text=text)
+    with pytest.raises(LoadError) as e:
+        loader.load_corpus(_write(tmp_path, rows))
+    msg = str(e.value)
+    assert "p0" in msg and reason in msg and text not in msg and "someone" not in msg
+
+
+def test_table_answers_load_and_need_a_prompt_id(tmp_path):
+    p = tmp_path / "t.jsonl"
+    p.write_text('{"prompt_id": "p0", "answer": null, "cues": [], "rows": [], "method": "m"}\n')
+    assert loader.load_table_answers(p)[0]["prompt_id"] == "p0"
+    p.write_text('{"answer": null}\n')
+    with pytest.raises(LoadError, match="prompt_id"):
+        loader.load_table_answers(p)
+
+
+# ---- paths and hashing
+
+def test_paths_on_a_temporary_root_stay_under_it_except_jevlib(tmp_path):
+    p = Paths(tmp_path)
+    for name in ("corpus", "selection_criteria", "labelling_record", "questions_py", "rule", "table_answers", "table_provenance",
+                 "manifest", "events", "ledger", "runs", "report", "decision_record", "rescores", "tests_dir"):
+        assert tmp_path in getattr(p, name).parents, name
+    assert all(tmp_path in c.parents for c in p.code_files())
+    assert tmp_path not in p.jevlib_dir.parents
+
+
+def test_jevlib_files_are_the_top_level_py_files_only(tmp_path):
+    d = tmp_path / "jevlib"
+    (d / "__pycache__").mkdir(parents=True)
+    (d / "sub").mkdir()
+    for f in ("b.py", "a.py", "notes.txt", "__pycache__/c.py", "sub/d.py"):
+        (d / f).write_text("x")
+    assert [f.name for f in Paths(tmp_path, jevlib_dir=d).jevlib_files()] == ["a.py", "b.py"]
+    assert all(f.parent == pathlib.Path(d) for f in Paths(tmp_path, jevlib_dir=d).jevlib_files())
+
+
+def test_sha256_file_is_the_sha256_of_the_bytes(tmp_path):
+    p = tmp_path / "f"
+    p.write_bytes(b"abc")
+    assert loader.sha256_file(p) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


Codegraph context
index_state: fresh
checked_at: 2026-11-26T16:38:23Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the files of this task are new or only used by later tasks; no dependent outside the touched files.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
