d784e95e408da85b9ccea0aa739ddd3c2ec75391
## family v2-severity-mapping
defect form: a reflect-category line is accepted although its severity/blocking pair cannot come from the spec's severity mapping (blocking -> MAJOR or CRITICAL with blocking true; minor -> MINOR).
command: grep -nE 'severity|blocking|SEVERITIES' src/superclaude/cli/review/findings_v2.py
before:
19:    SEVERITIES,
27:    "severity",
28:    "blocking",
103:    if not _one_of(obj.get("severity"), SEVERITIES):
104:        return "severity must be CRITICAL, MAJOR or MINOR"
105:    if not isinstance(obj.get("blocking"), bool):
106:        return "blocking must be a boolean"
107:    if obj["blocking"] and obj["severity"] == "MINOR":
108:        return "a MINOR finding cannot be blocking"
coupled sites: the tests that use severity/blocking with reflect_category in tests/review/test_review_findings_v2.py; the docstring of check_finding.

after:
19:    SEVERITIES,
27:    "severity",
28:    "blocking",
103:    if not _one_of(obj.get("severity"), SEVERITIES):
104:        return "severity must be CRITICAL, MAJOR or MINOR"
105:    if not isinstance(obj.get("blocking"), bool):
106:        return "blocking must be a boolean"
107:    if obj["blocking"] and obj["severity"] == "MINOR":
108:        return "a MINOR finding cannot be blocking"
161:        if obj["blocking"] != (obj["severity"] != "MINOR"):
162:            return "with reflect_category set, a MAJOR or CRITICAL finding must be blocking and a MINOR one must not"
