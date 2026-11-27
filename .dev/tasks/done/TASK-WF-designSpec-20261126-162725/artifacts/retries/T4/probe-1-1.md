223bda41860ac06ef72c4795b2dbcd2f457b9e3e

## family evidence-hash
defect form: an event line is written with a null evidence path or hash (an append_event call with no evidence, or an evidence path that is not a file)
command: grep -n -E -e 'append_event\(|evidence' -- .dev/research/jev-vs-keyword-table-611/harness/events.py .dev/research/jev-vs-keyword-table-611/harness/gate.py .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py
before:
  .dev/research/jev-vs-keyword-table-611/harness/events.py:4:  events.py owner-input --evidence PATH --note TEXT
  .dev/research/jev-vs-keyword-table-611/harness/events.py:27:_CORE = ("ts", "event", "evidence", "evidence_sha256")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:30:def _evidence_path(paths, evidence):
  .dev/research/jev-vs-keyword-table-611/harness/events.py:31:    p = pathlib.Path(evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:38:def append_event(paths, event, evidence=None, **fields):
  .dev/research/jev-vs-keyword-table-611/harness/events.py:39:    """Append one event line (sorted keys, UTC timestamp, the evidence path and the evidence file's SHA-256) and return it."""
  .dev/research/jev-vs-keyword-table-611/harness/events.py:46:    if evidence is not None:
  .dev/research/jev-vs-keyword-table-611/harness/events.py:47:        ev_path = _evidence_path(paths, evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:48:        if pathlib.Path(evidence).is_file():
  .dev/research/jev-vs-keyword-table-611/harness/events.py:49:            ev_sha = loader.sha256_file(evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:51:           "evidence": ev_path, "evidence_sha256": ev_sha, **fields}
  .dev/research/jev-vs-keyword-table-611/harness/events.py:77:    a.add_argument("--evidence", required=True)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:89:        ev = pathlib.Path(args.evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:92:        rec = append_event(paths, "owner_input_received", evidence=ev, note=args.note)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:96:        rec = append_event(paths, "price_confirmed", usd_per_mtok=args.usd_per_mtok, source=args.source)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:100:        rec = append_event(paths, "lead_go", evidence=paths.rule, rule_sha256=loader.sha256_file(paths.rule), words=args.words)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:169:    events.append_event(paths, "gate1", passed=not failed, failed=failed)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:176:    events.append_event(paths, "gate2", passed=not failed, failed=failed)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:189:    events.append_event(paths, "freeze", evidence=paths.corpus, what="corpus", prompts=len(rows))
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:203:    events.append_event(paths, "freeze", evidence=paths.table_answers, what="table")
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:211:    events.append_event(paths, "rule_freeze", evidence=paths.rule)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:230:    return events.append_event(paths, "tests_passed", command=" ".join(cmd), count=count, code_hashes=_code_hashes(paths))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:29:        events.append_event(p, "price_confirmed", usd_per_mtok=price, source="test")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:33:        events.append_event(p, "lead_go", evidence=p.rule, rule_sha256=loader.sha256_file(p.rule), words="go")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:106:    events.append_event(exp, "lead_go", rule_sha256="0" * 64, words="old")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:131:    events.append_event(exp, event)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:238:# ---- events (append-only, evidence, the three commands)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:241:    first = events.append_event(exp, "freeze", evidence=exp.corpus, what="corpus")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:243:    events.append_event(exp, "gate1", passed=True, failed=[])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:246:    assert first["evidence"] == "corpus/corpus.jsonl" and first["evidence_sha256"] == loader.sha256_file(exp.corpus)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:254:        events.append_event(exp, "made_up")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:256:        events.append_event(exp, "gate1", ts="now")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:262:    assert events.main(["owner-input", "--evidence", str(note), "--note", "owner set the operators", "--root", str(exp.root)]) == 0
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:267:    assert got["owner_input_received"]["evidence_sha256"] == loader.sha256_file(note)
coupled sites: events.py:38-57 (append_event) and :88-92 (owner-input CLI); gate.py:169, :176, :230 (gate1, gate2, tests_passed events); events.py:96 (price); tests/test_gate_events.py:29, :106, :131, :243, :262 (event writers in tests) and :240-249 (the AC6 test)
after:
  .dev/research/jev-vs-keyword-table-611/harness/events.py:4:  events.py owner-input --evidence PATH --note TEXT
  .dev/research/jev-vs-keyword-table-611/harness/events.py:27:_CORE = ("ts", "event", "evidence", "evidence_sha256")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:30:def _evidence_path(paths, evidence):
  .dev/research/jev-vs-keyword-table-611/harness/events.py:31:    p = pathlib.Path(evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:38:def append_event(paths, event, evidence=None, **fields):
  .dev/research/jev-vs-keyword-table-611/harness/events.py:39:    """Append one event line (sorted keys, UTC timestamp, the evidence path and the evidence file's SHA-256) and return it.
  .dev/research/jev-vs-keyword-table-611/harness/events.py:41:    An event with no evidence of its own is tied to the rule file in force when it was written, so the line still carries a path
  .dev/research/jev-vs-keyword-table-611/harness/events.py:42:    and a hash.  An evidence path that is not a file is refused.  Only a log with no rule file yet leaves both null.
  .dev/research/jev-vs-keyword-table-611/harness/events.py:49:    if evidence is None and paths.rule.is_file():
  .dev/research/jev-vs-keyword-table-611/harness/events.py:50:        evidence = paths.rule
  .dev/research/jev-vs-keyword-table-611/harness/events.py:52:    if evidence is not None:
  .dev/research/jev-vs-keyword-table-611/harness/events.py:53:        if not pathlib.Path(evidence).is_file():
  .dev/research/jev-vs-keyword-table-611/harness/events.py:54:            raise ValueError(f"evidence file does not exist: {evidence}")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:55:        ev_path = _evidence_path(paths, evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:56:        ev_sha = loader.sha256_file(evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:58:           "evidence": ev_path, "evidence_sha256": ev_sha, **fields}
  .dev/research/jev-vs-keyword-table-611/harness/events.py:84:    a.add_argument("--evidence", required=True)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:96:        ev = pathlib.Path(args.evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:100:            ap.error(f"--evidence {args.evidence} is not a file")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:101:        rec = append_event(paths, "owner_input_received", evidence=ev, note=args.note)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:105:        rec = append_event(paths, "price_confirmed", usd_per_mtok=args.usd_per_mtok, source=args.source)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:109:        rec = append_event(paths, "lead_go", evidence=paths.rule, rule_sha256=loader.sha256_file(paths.rule), words=args.words)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:170:    events.append_event(paths, "gate1", passed=not failed, failed=failed)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:177:    events.append_event(paths, "gate2", passed=not failed, failed=failed)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:190:    events.append_event(paths, "freeze", evidence=paths.corpus, what="corpus", prompts=len(rows))
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:204:    events.append_event(paths, "freeze", evidence=paths.table_answers, what="table")
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:212:    events.append_event(paths, "rule_freeze", evidence=paths.rule)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:240:    return events.append_event(paths, "tests_passed", command=" ".join(cmd), count=count, code_hashes=_code_hashes(paths))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:30:        events.append_event(p, "price_confirmed", usd_per_mtok=price, source="test")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:34:        events.append_event(p, "lead_go", evidence=p.rule, rule_sha256=loader.sha256_file(p.rule), words="go")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:107:    events.append_event(exp, "lead_go", rule_sha256="0" * 64, words="old")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:132:    events.append_event(exp, event)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:244:# ---- events (append-only, evidence, the three commands)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:247:    first = events.append_event(exp, "freeze", evidence=exp.corpus, what="corpus")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:249:    events.append_event(exp, "gate1", passed=True, failed=[])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:252:    assert first["evidence"] == "corpus/corpus.jsonl" and first["evidence_sha256"] == loader.sha256_file(exp.corpus)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:262:    events.append_event(exp, "first_request")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:267:        assert e["ts"] and e["evidence"], e["event"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:268:        assert re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]), e["event"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:269:    assert events.latest(exp, "gate2")["evidence"] == "decision-rule.md"          # no evidence of its own: tied to the rule file
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:272:def test_an_evidence_path_that_is_not_a_file_is_refused(exp, tmp_path):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:274:        events.append_event(exp, "freeze", evidence=tmp_path / "nope.txt")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:276:        events.main(["owner-input", "--evidence", str(tmp_path / "nope.txt"), "--note", "x", "--root", str(exp.root)])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:282:        events.append_event(exp, "made_up")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:284:        events.append_event(exp, "gate1", ts="now")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:290:    assert events.main(["owner-input", "--evidence", str(note), "--note", "owner set the operators", "--root", str(exp.root)]) == 0
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:295:    assert got["owner_input_received"]["evidence_sha256"] == loader.sha256_file(note)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:298:    assert all(e["evidence"] and re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]) for e in got.values())

## family rule-copy
defect form: a test or fixture reads the live decision-rule.md and depends on its three open fields still being UNSET
command: grep -n -E -e 'decision-rule|load_rule|UNSET|RULE\b|rule_copy' -- .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py .dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py
before:
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:93:    p.rule.write_text(loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8"), encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:16:    s = s.replace("noul_low_operator: UNSET", f"noul_low_operator: {low}").replace("noul_high_operator: UNSET", f"noul_high_operator: {high}")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:17:    p.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", f"unresolved_failure_invalid_count: {count}"), encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:51:    assert "UNSET" in exp.rule.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:112:    exp.rule.write_text(exp.rule.read_text(encoding="utf-8").replace("noul_low_operator: le", "noul_low_operator: UNSET"), encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:192:    with pytest.raises(loader.LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:8:RULE = loader.EXPERIMENT / "decision-rule.md"
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:12:def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:13:    s = RULE.read_text(encoding="utf-8") if text is None else text
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:19:    p = tmp_path / "decision-rule.md"
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:27:    rule = loader.load_rule(RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:28:    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} == OPEN_FIELDS
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:34:    text = RULE.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:43:        loader.load_rule(_rule_copy(tmp_path, "status: AGREED", f"status: {status}"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:47:    s = RULE.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:50:    p = _rule_copy(tmp_path, text=head + "## Agreement text (verbatim)\n\n## Relayed owner words" + tail)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:52:        loader.load_rule(p)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:57:    lines = [(f"{key}:" if line.startswith(key + ":") else line) for line in RULE.read_text(encoding="utf-8").splitlines()]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:58:    p = _rule_copy(tmp_path, text="\n".join(lines) + "\n")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:60:        loader.load_rule(p)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:65:        loader.load_rule(_rule_copy(tmp_path, drop_line="alpha_inverse:"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:67:        loader.load_rule(tmp_path / "nope.md")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:71:    with pytest.raises(LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:72:        loader.load_rule(RULE, for_scoring=True)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:73:    s = RULE.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:74:    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:75:    s = s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:76:    rule = loader.load_rule(_rule_copy(tmp_path, text=s), for_scoring=True)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:82:        loader.load_rule(_rule_copy(tmp_path, "noul_low_operator: UNSET", "noul_low_operator: gt"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:84:        loader.load_rule(_rule_copy(tmp_path, "noul_high_operator: UNSET", "noul_high_operator: lt"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:83:@pytest.mark.parametrize("low_op,high_op", [("UNSET", "ge"), ("le", "UNSET"), ("gt", "ge"), ("le", "lt")])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:109:RULE = {"attempt_timeout_s": 10.0, "median_population": "answered_only"}
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:114:    s = latency_stats(attempts, RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:119:    s = latency_stats([_a("p1", 0.5), _a("p2", 2.0, answered=False)], RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:124:    rule = dict(RULE, median_population="include_timeouts_at_cap")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:130:    assert latency_stats([], RULE) == {"median": None, "slowest": None, "p90": None, "n": 0}
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:132:        latency_stats([_a("p1", 1.0)], dict(RULE, median_population="all"))
coupled sites: tests/conftest.py:93 (exp fixture copy); tests/test_gate_events.py:16-17 (fill_rule), :51, :112, :192; tests/test_loader.py:12-13 (_rule_copy), :28, :71-76, :82, :84. tests/test_scorer_core.py:83 passes the string UNSET as a parameter and does not read the file (not coupled). test_loader.py is a Task 2 file: listed here so the sibling edit is in scope
after:
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:63:    """The committed rule file with its three open fields forced back to ``UNSET``, so a test never depends on whether the owner
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:68:    text = loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:69:    return re.sub(r"^(noul_low_operator|noul_high_operator|unresolved_failure_invalid_count): .*$", r"\1: UNSET", text,
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:84:    a copy of the committed rule file with its open fields set to UNSET.  Nothing here touches the real experiment folder."""
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:17:    s = s.replace("noul_low_operator: UNSET", f"noul_low_operator: {low}").replace("noul_high_operator: UNSET", f"noul_high_operator: {high}")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:18:    p.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", f"unresolved_failure_invalid_count: {count}"), encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:52:    assert "UNSET" in exp.rule.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:113:    exp.rule.write_text(exp.rule.read_text(encoding="utf-8").replace("noul_low_operator: le", "noul_low_operator: UNSET"), encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:193:    with pytest.raises(loader.LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:269:    assert events.latest(exp, "gate2")["evidence"] == "decision-rule.md"          # no evidence of its own: tied to the rule file
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:9:RULE = loader.EXPERIMENT / "decision-rule.md"
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:13:def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:14:    """A copy of the rule file with its open fields UNSET (unless ``text`` is given), whatever the live file holds now."""
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:21:    p = tmp_path / "decision-rule.md"
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:29:    rule = loader.load_rule(RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:30:    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} <= OPEN_FIELDS
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:31:    normal = loader.load_rule(_rule_copy(tmp_path))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:32:    assert {k for k in loader.RULE_KEYS if normal[k] == "UNSET"} == OPEN_FIELDS
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:38:    text = RULE.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:47:        loader.load_rule(_rule_copy(tmp_path, "status: AGREED", f"status: {status}"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:51:    s = RULE.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:54:    p = _rule_copy(tmp_path, text=head + "## Agreement text (verbatim)\n\n## Relayed owner words" + tail)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:56:        loader.load_rule(p)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:61:    lines = [(f"{key}:" if line.startswith(key + ":") else line) for line in RULE.read_text(encoding="utf-8").splitlines()]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:62:    p = _rule_copy(tmp_path, text="\n".join(lines) + "\n")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:64:        loader.load_rule(p)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:69:        loader.load_rule(_rule_copy(tmp_path, drop_line="alpha_inverse:"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:71:        loader.load_rule(tmp_path / "nope.md")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:75:    with pytest.raises(LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:76:        loader.load_rule(_rule_copy(tmp_path), for_scoring=True)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:78:    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:79:    s = s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:80:    rule = loader.load_rule(_rule_copy(tmp_path, text=s), for_scoring=True)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:86:        loader.load_rule(_rule_copy(tmp_path, "noul_low_operator: UNSET", "noul_low_operator: gt"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:88:        loader.load_rule(_rule_copy(tmp_path, "noul_high_operator: UNSET", "noul_high_operator: lt"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:83:@pytest.mark.parametrize("low_op,high_op", [("UNSET", "ge"), ("le", "UNSET"), ("gt", "ge"), ("le", "lt")])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:109:RULE = {"attempt_timeout_s": 10.0, "median_population": "answered_only"}
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:114:    s = latency_stats(attempts, RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:119:    s = latency_stats([_a("p1", 0.5), _a("p2", 2.0, answered=False)], RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:124:    rule = dict(RULE, median_population="include_timeouts_at_cap")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:130:    assert latency_stats([], RULE) == {"median": None, "slowest": None, "p90": None, "n": 0}
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:132:        latency_stats([_a("p1", 1.0)], dict(RULE, median_population="all"))

## family record-command
defect form: the command recorded and run by record-tests differs from the plan Constraints form (repo-relative tests folder, -v)
command: grep -n -E -e 'pytest| -q| -v' -- .dev/research/jev-vs-keyword-table-611/harness/gate.py .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py
before:
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:222:    cmd = ["uv", "run", "pytest", str(paths.tests_dir), "-q"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:4:import pytest
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:59:@pytest.mark.parametrize("edit,name", [
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:81:@pytest.mark.parametrize("attr,name", [("corpus", "hash_corpus"), ("selection_criteria", "hash_selection_criteria"),
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:97:@pytest.mark.parametrize("skip,name", [("go", "go_missing"), ("tests", "tests_not_recorded"), ("rule", "rule_not_frozen"),
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:128:@pytest.mark.parametrize("event", ["first_request", "run_end"])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:177:        with pytest.raises(GateError, match="already holds"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:192:    with pytest.raises(loader.LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:198:    with pytest.raises(GateError, match="Gate 1"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:202:    with pytest.raises(GateError, match="missing"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:210:    with pytest.raises(loader.LoadError, match="privacy"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:215:@pytest.mark.parametrize("result,match", [((1, "1 failed, 3 passed"), "failed"), ((0, "no tests ran"), "no tests")])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:217:    with pytest.raises(GateError, match=match):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:224:    assert rec["count"] == 12 and rec["command"].startswith("uv run pytest ") and rec["command"].endswith(" -q")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:253:    with pytest.raises(ValueError):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:255:    with pytest.raises(ValueError):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:273:    with pytest.raises(SystemExit):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:289:    assert spend.worst_case_usd(1_000_000, 0.042) == pytest.approx(0.042)
coupled sites: gate.py:222 (the command built), gate.py:230 (the command written to the event), tests/test_gate_events.py:224 (the assertion on the recorded command)
after:
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:222:    """``uv run pytest <tests folder> -v``, the folder relative to the repository root when it is under it."""
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:227:    return ["uv", "run", "pytest", folder, "-v"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:5:import pytest
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:60:@pytest.mark.parametrize("edit,name", [
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:82:@pytest.mark.parametrize("attr,name", [("corpus", "hash_corpus"), ("selection_criteria", "hash_selection_criteria"),
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:98:@pytest.mark.parametrize("skip,name", [("go", "go_missing"), ("tests", "tests_not_recorded"), ("rule", "rule_not_frozen"),
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:129:@pytest.mark.parametrize("event", ["first_request", "run_end"])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:178:        with pytest.raises(GateError, match="already holds"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:193:    with pytest.raises(loader.LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:199:    with pytest.raises(GateError, match="Gate 1"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:203:    with pytest.raises(GateError, match="missing"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:211:    with pytest.raises(loader.LoadError, match="privacy"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:216:@pytest.mark.parametrize("result,match", [((1, "1 failed, 3 passed"), "failed"), ((0, "no tests ran"), "no tests")])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:218:    with pytest.raises(GateError, match=match):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:225:    assert rec["count"] == 12 and rec["command"].startswith("uv run pytest ") and rec["command"].endswith(" -v")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:232:    assert gate._tests_command(loader.Paths()) == ["uv", "run", "pytest", ".dev/research/jev-vs-keyword-table-611/harness/tests", "-v"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:273:    with pytest.raises(ValueError, match="does not exist"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:275:    with pytest.raises(SystemExit):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:281:    with pytest.raises(ValueError):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:283:    with pytest.raises(ValueError):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:302:    with pytest.raises(SystemExit):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:318:    assert spend.worst_case_usd(1_000_000, 0.042) == pytest.approx(0.042)

## family docstring
defect form: the module docstring says Gate 2's pass is what the lead's go rests on, but the code requires the lead_go before Gate 2 can pass
command: grep -n -i -E -e "lead's go|lead_go|go_missing|rests on" -- .dev/research/jev-vs-keyword-table-611/harness/gate.py .dev/research/jev-vs-keyword-table-611/harness/events.py
before:
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:9:  gate.py gate2           everything Gate 1 checks, plus the rest; its pass is what the lead's go rests on
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:156:    go = events.latest(paths, "lead_go")
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:158:        failed.append("go_missing")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:25:EVENTS = ("owner_input_received", "freeze", "rule_freeze", "gate1", "gate2", "tests_passed", "price_confirmed", "lead_go",
  .dev/research/jev-vs-keyword-table-611/harness/events.py:74:    ap = argparse.ArgumentParser(prog="events.py", description="record owner input, the confirmed price and the lead's go")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:82:    c = sub.add_parser("go", help="record the lead's go, naming the rule file's current hash")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:100:        rec = append_event(paths, "lead_go", evidence=paths.rule, rule_sha256=loader.sha256_file(paths.rule), words=args.words)
coupled sites: gate.py:9 (docstring line); gate.py:156-160 (go_missing, go_rule_hash); events.py:74 and :82 (lead's go wording in help text, which is accurate and stays)
after:
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:9:  gate.py gate2           everything Gate 1 checks, plus the rest; a pass is what the live run rests on (a lead_go that names the
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:157:    go = events.latest(paths, "lead_go")
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:159:        failed.append("go_missing")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:25:EVENTS = ("owner_input_received", "freeze", "rule_freeze", "gate1", "gate2", "tests_passed", "price_confirmed", "lead_go",
  .dev/research/jev-vs-keyword-table-611/harness/events.py:81:    ap = argparse.ArgumentParser(prog="events.py", description="record owner input, the confirmed price and the lead's go")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:89:    c = sub.add_parser("go", help="record the lead's go, naming the rule file's current hash")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:109:        rec = append_event(paths, "lead_go", evidence=paths.rule, rule_sha256=loader.sha256_file(paths.rule), words=args.words)

