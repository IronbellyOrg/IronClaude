from superclaude.pr_submit import finding_from_comment
base = {"path": "a.py", "line": 3, "body": "bug"}
f = finding_from_comment({**base, "reviewer": "codex", "severity_hint": "medium"})
print("codex reviewer:", f.reviewer, "hint:", f.severity_hint)
print("default reviewer:", finding_from_comment(base).reviewer)
try:
    finding_from_comment({**base, "reviewer": 7})
    print("non-text reviewer: accepted (unexpected)")
except ValueError as exc:
    print("non-text reviewer: ValueError", exc)
assert f.reviewer == "codex" and finding_from_comment(base).reviewer == "augment"
