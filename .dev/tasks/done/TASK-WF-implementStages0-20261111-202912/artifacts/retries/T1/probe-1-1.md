d784e95e408da85b9ccea0aa739ddd3c2ec75391
## family v2-table-rule-coverage-rows
defect form: a table rule of the "Finding format" table (coverage_rows must be ids in the Coverage slice) is parsed but not enforced.
command: grep -nE 'coverage_rows|assigned_rows' src/superclaude/cli/review/findings_v2.py tests/review/test_review_findings_v2.py
before:
src/superclaude/cli/review/findings_v2.py:130:    rows = obj.get("coverage_rows")
src/superclaude/cli/review/findings_v2.py:134:        return "coverage_rows must be a list of strings"
src/superclaude/cli/review/findings_v2.py:148:    assigned_rows: Iterable[str] = (),
src/superclaude/cli/review/findings_v2.py:155:    assigned_rows is non-empty and the card's coverage observations (observed_rows) cover every
src/superclaude/cli/review/findings_v2.py:209:        assigned = set(assigned_rows)
tests/review/test_review_findings_v2.py:111:    r = v2.parse_block(empty, assigned_rows=["R1", "R2"], observed_rows=["R1"])
tests/review/test_review_findings_v2.py:113:    r = v2.parse_block(empty, assigned_rows=["R1", "R2"], observed_rows=["R2", "R1"])
tests/review/test_review_findings_v2.py:173:        {"coverage_rows": "R1"},
tests/review/test_review_findings_v2.py:177:    good = json.loads(line(self_confidence=0.7, coverage_rows=["R1"], channel="advisory"))
coupled sites: the test_review_findings_v2.py cases for coverage_rows and the module docstring.
## family v2-table-rule-citation-path
defect form: a citation field rule (path repo-relative) is only checked for non-emptiness.
command: grep -nE '_check_citation|"path"' src/superclaude/cli/review/findings_v2.py tests/review/test_review_findings_v2.py
before:
src/superclaude/cli/review/findings_v2.py:44:def _check_citation(c: Any) -> str | None:
src/superclaude/cli/review/findings_v2.py:49:    path = c.get("path")
src/superclaude/cli/review/findings_v2.py:99:            err = _check_citation(c)
tests/review/test_review_findings_v2.py:32:CITE = {"role": "plan", "path": "plan.md", "line_start": 3, "line_end": 4}
tests/review/test_review_findings_v2.py:143:        [{**CITE, "path": ""}],
coupled sites: test_bad_citations_rejected and any fixture citation path.

after (coverage rows family):
src/superclaude/cli/review/findings_v2.py:132:    rows = obj.get("coverage_rows")
src/superclaude/cli/review/findings_v2.py:136:        return "coverage_rows must be a list of strings"
src/superclaude/cli/review/findings_v2.py:150:    assigned_rows: Iterable[str] = (),
src/superclaude/cli/review/findings_v2.py:157:    assigned_rows is non-empty and the card's coverage observations (observed_rows) cover every
src/superclaude/cli/review/findings_v2.py:160:    assigned_set = set(assigned_rows)
src/superclaude/cli/review/findings_v2.py:206:            extra = [r for r in obj.get("coverage_rows") or [] if r not in assigned_set]
src/superclaude/cli/review/findings_v2.py:208:                err = "coverage_rows names ids outside the assigned Coverage slice: " + ", ".join(extra)
tests/review/test_review_findings_v2.py:111:    r = v2.parse_block(empty, assigned_rows=["R1", "R2"], observed_rows=["R1"])
tests/review/test_review_findings_v2.py:113:    r = v2.parse_block(empty, assigned_rows=["R1", "R2"], observed_rows=["R2", "R1"])
tests/review/test_review_findings_v2.py:157:def test_coverage_rows_must_be_in_assigned_slice():
tests/review/test_review_findings_v2.py:158:    ok = report(line(coverage_rows=["R1"]))
tests/review/test_review_findings_v2.py:159:    bad = report(line(coverage_rows=["R1", "R9"]))
tests/review/test_review_findings_v2.py:160:    assert v2.parse_block(ok, assigned_rows=["R1", "R2"])["ok"] is True
tests/review/test_review_findings_v2.py:161:    r = v2.parse_block(bad, assigned_rows=["R1", "R2"])
tests/review/test_review_findings_v2.py:185:        {"coverage_rows": "R1"},
tests/review/test_review_findings_v2.py:189:    good = json.loads(line(self_confidence=0.7, coverage_rows=["R1"], channel="advisory"))
after (citation path family):
src/superclaude/cli/review/findings_v2.py:44:def _check_citation(c: Any) -> str | None:
src/superclaude/cli/review/findings_v2.py:49:    path = c.get("path")
src/superclaude/cli/review/findings_v2.py:101:            err = _check_citation(c)
tests/review/test_review_findings_v2.py:32:CITE = {"role": "plan", "path": "plan.md", "line_start": 3, "line_end": 4}
tests/review/test_review_findings_v2.py:143:        [{**CITE, "path": ""}],
tests/review/test_review_findings_v2.py:144:        [{**CITE, "path": "/etc/passwd"}],
tests/review/test_review_findings_v2.py:145:        [{**CITE, "path": "../outside.md"}],
tests/review/test_review_findings_v2.py:146:        [{**CITE, "path": "a/../../b.md"}],
