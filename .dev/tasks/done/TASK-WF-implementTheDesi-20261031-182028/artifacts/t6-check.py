from superclaude.pr_submit import DetectionContract, finding_from_comment, remap_severity, route
from superclaude.pr_submit.reviewers import (REVIEWERS, codex_severity_hint, parse_codex_priority,
    retrigger_phrase, reviewer_activity, reviewer_identities)

def badge(alt, url, title="Fix it"):
    return (f"**<sub><sub>![{alt} Badge](https://img.shields.io/badge/{url}-yellow?style=flat)"
            f"</sub></sub>  {title}**\n\nBody text.\n\n<!-- codex-code-review-finding:v1 -->")

cases = {"P0": badge("P0", "P0"), "P1": badge("P1", "P1"), "P2": badge("P2", "P2"), "P3": badge("P3", "P3"),
         "no badge": "**Fix it**\n\nBody.", "two badges": badge("P1", "P1") + "\n" + badge("P2", "P2"),
         "P4": badge("P4", "P4"), "alt/url mismatch": badge("P1", "P2"),
         "badge not on first line": "Intro line\n" + badge("P2", "P2")}
expected = {"P0": "P0", "P1": "P1", "P2": "P2", "P3": "P3"}
ok = True
for name, body in cases.items():
    got = parse_codex_priority(body)
    want = expected.get(name)
    ok &= got == want
    hint = codex_severity_hint(got)
    r = route(remap_severity(finding_from_comment({"path": "a.py", "line": 1, "body": body,
                                                   "reviewer": "codex", "severity_hint": hint})))
    print(f"{name:24} priority={got} hint={hint} route={r}")
shipped = DetectionContract.load()
print("REVIEWERS", REVIEWERS)
print("codex identities", sorted(reviewer_identities(shipped, "codex")), "augment", sorted(reviewer_identities(shipped, "augment")))
print("phrases", retrigger_phrase(shipped, "augment"), "|", retrigger_phrase(shipped, "codex"))
print("bare contract codex identities", reviewer_identities(DetectionContract(), "codex"))
p = {"reviews": [], "comments": [{"user": {"login": "chatgpt-codex-connector[bot]"}, "body": "x"}]}
print("activity", reviewer_activity(p, shipped))
raise SystemExit(0 if ok else 1)
